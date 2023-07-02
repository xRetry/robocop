import rclpy
from typing import Generator, List
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Float64
import numpy as np
import time

class PubNode(Node):
    def __init__(self, topic: str, publish_value: float=10, publish_rate_sec: float=1):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(Float64, topic, 10) # TODO: Set correct message type
        self.timer = self.create_timer(publish_rate_sec, self.timer_callback)
        self.publish_value = publish_value

    def timer_callback(self):
        msg = Float64()
        msg.data = self.publish_value

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


class SubNode(Node):
    def __init__(self, topic: str, values_out: list):
        super().__init__('subscriber')
        self.subscriber = self.create_subscription(Float64, topic, self.sub_callback, qos_profile=qos_profile_sensor_data) # TODO: Set correct message type

    def sub_callback(self, msg):
        self.get_logger().info('Receiving: "%s"' % msg.data)


class RosNode():
    def __init__(self, pub_topic: str, sub_topics: List[str], pub_rate_sec: float):
        rclpy.init()
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(PubNode(pub_topic, 10, pub_rate_sec))

        self.values = {}
        for topic in sub_topics:
            self.values[topic] = []
            self.executor.add_node(SubNode(topic, self.values[topic]))

    def save_data():
        # TODO: Store data to file
        pass

    def start():
        executor.spin()

    def stop():
        executor.shutdown()
        pub.destroy_node()
        sub.destroy_node()


def main():
    pass


if __name__ == '__main__':
    main()
