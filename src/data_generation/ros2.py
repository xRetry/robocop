import rclpy
from typing import Generator, List
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import qos_profile_sensor_data
import numpy as np
import time

class PubNode(Node):
    def __init__(self, topic: str, gen: Generator, publish_rate_sec: float):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(PinValues, topic, 10) # TODO: Set correct message type
        self.timer = self.create_timer(publish_rate_sec, self.timer_callback)
        self.data_gen = gen

    def timer_callback(self):
        msg = PinValues()

        msg.values = np.zeros(36)
        val = next(self.data_gen)
        self.vals.append([time.time(), val])
        msg.values[self.pin_out] = val
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.values)


class SubNode(Node):
    def __init__(self, topic: str, values_out: list):
        super().__init__('subscriber')
        self.subscriber = self.create_subscription(PinValues, topic, self.sub_callback, qos_profile=qos_profile_sensor_data) # TODO: Set correct message type
        self.values = values_out

    def sub_callback(self, msg):
        self.values.append(msg)


class RosNode():
    def __init__(self, pub_topic: str, sub_topics: List[str], pub_rate_sec: float):
        rclpy.init()
        executor = SingleThreadedExecutor()
        executor.add_node(PubNode(pub_topic, 10, pub_rate_sec))

        self.values = {}
        for topic in topics:
            self.values[topic] = []
            executor.add_node(SubNode(topic, self.values[topic]))

    def save_data():
        # TODO: Store data to file
        pass

    def start():
        executor.spin()

    def stop():
        executor.shutdown()
        pub.destroy_node()
        sub.destroy_node()


if __name__ == '__main__':
    main()
