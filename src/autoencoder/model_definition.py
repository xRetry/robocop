import tensorflow as tf
from tensorflow import keras
from keras import Model 
from keras.layers import Dense, Input, Layer
import keras_tuner as kt

class Sampling(Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

class VAE(Model):
    def __init__(self, encoder, decoder, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(
            name="reconstruction_loss"
        )
        self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)
            reconstruction_loss = tf.reduce_mean(
                tf.reduce_sum(
                    keras.losses.binary_crossentropy(data, reconstruction), axis=None
                )
            )
            kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
            kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=1))
            total_loss = reconstruction_loss + kl_loss
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }

def build_vae(input_size: int, hp: kt.HyperParameters) -> Model:
    """Defines the architecture of the VAE and returns the compiled model."""

    dim_input = input_size
    dim_latent: int = hp.Int("latent dim", min_value=2, max_value=500)
    num_dense: int = hp.Int("dense amount", min_value=1, max_value=20)
    size_dense: int = hp.Int("dense size", min_value=10, max_value=1000)
    lr: float = hp.Float("learning rate", min_value=1e-6, max_value=1e-2, sampling="log")

    encoder_inputs = x = Input(shape=dim_input)

    for _ in range(num_dense):
        x = Dense(size_dense, activation="relu")(x)

    z_mean = Dense(dim_latent, name="z_mean")(x)
    z_log_var = Dense(dim_latent, name="z_log_var")(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")

    latent_inputs = x = Input(shape=dim_latent)
    for _ in range(num_dense):
        x = Dense(size_dense, activation="relu")(x)

    decoder_outputs = Dense(dim_input, activation="sigmoid")(x)
    decoder = Model(latent_inputs, decoder_outputs, name="decoder")

    vae = VAE(encoder, decoder)
    vae.compile(optimizer=keras.optimizers.Adam(learning_rate=lr))
    return vae


