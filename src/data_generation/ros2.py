import rclpy
from typing import Dict
from threading import Event
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist


class PubNode(Node):
    def __init__(self, topic: str, publish_value: float=10, publish_rate_sec: float=1):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(Twist, topic, 10) # TODO: Set correct message type
        self.timer = self.create_timer(publish_rate_sec, self.timer_callback)
        self.publish_value = publish_value

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = float(self.publish_value)
        msg.angular.z = float(0)

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.linear)


class SubNode(Node):
    def __init__(self, topic: str, MsgType: type, values: list):
        super().__init__('subscriber')
        self.subscriber = self.create_subscription(MsgType, topic, self.sub_callback, qos_profile=qos_profile_sensor_data)
        self.values = values

    def sub_callback(self, msg):
        self.get_logger().info('Receiving: "%s"' % msg.data)
        self.values.append(msg.data)


class RosNode():
    def __init__(self, pub_topic: str, topic_msg_map: Dict[str, type], pub_rate_sec: float, save_event: Event|None=None, stop_event: Event|None=None):
        rclpy.init()
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(PubNode(pub_topic, 0.5, pub_rate_sec))
        self.save_event = save_event if save_event is not None else Event();
        self.stop_event = stop_event if stop_event is not None else Event();

        self.values = {}
        for topic, MsgType in topic_msg_map.items():
            self.values[topic] = []
            self.executor.add_node(SubNode(topic, MsgType, self.values[topic]))

    def save_data(self):
        # TODO: Store data to file
        print(self.values)
        for vals in self.values.values():
            vals = []

    def start(self):
        while not self.stop_event.is_set():
            self.save_event.set()
            while self.save_event.is_set() and not self.stop_event.is_set():
                self.executor.spin_once()

            self.save_data()
        self.stop()

    def stop(self):
        self.executor.shutdown()


def main():
    pass

if __name__ == '__main__':
    main()
