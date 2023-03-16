"""
This file is used to generate sensor data using a robotic simulator.

The planned methodology assumes the simulator API provides the following functionality:
- Accessing the world/enviroment objects
- Placing a robot at a specific location
- Starting the simulation
- Accessing the robots sensor readings

So far, the file only contains the outline. Implementation details are missing.
"""

import datetime
import numpy as np
import pandas as pd


def create_env():
    """Creates a world with some objects inside."""

    # TODO: Implement
    return None


def is_colliding(robot_coords: np.ndarray, env) -> bool:
    """Checks if the roboter is inside an object given its coordinates."""

    # TODO: Implement
    return False

def sample_env(env) -> np.ndarray:
    """Randomly places the roboter inside the world and extracts the sensor values."""

    robot_coords = np.random(2)
    while is_colliding(robot_coords=robot_coords, env=env):
        robot_coords = np.random(2)

    # TODO: Execute the actual simulation and extract sensor values
    return np.zeros(10)

def main():
    NUM_SAMPLES = 50
    env = create_env()

    # NOTE: Using map to be able to use multiprocessing later on.
    # The default map can be easily replaced with imap_unordered.
    # TODO: The enviroment object either needs to be thread safe or copied for each thead.
    envs = [env]*NUM_SAMPLES
    samples = list(map(sample_env, envs))

    # NOTE: Maybe it is possible to write to the file directly from the threads.
    # Then the dataframe conversion can be skipped.
    df = pd.DataFrame(samples)
    time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_parquet(f"../../data/static/data_static_{time_str}.parquet")


if __name__ == "__main__":
    main()
