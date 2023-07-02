import rclpy
from typing import Dict
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image, LaserScan
from actuator_msgs.msg import ActuatorsAngularVelocity


class PubNode(Node):
    def __init__(self, topic: str, publish_value: float=10, publish_rate_sec: float=1):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(ActuatorsAngularVelocity, topic, 10) # TODO: Set correct message type
        self.timer = self.create_timer(publish_rate_sec, self.timer_callback)
        self.publish_value = publish_value

    def timer_callback(self):
        msg = ActuatorsAngularVelocity()
        msg.velocity = self.publish_value

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.velocity)


class SubNode(Node):
    def __init__(self, topic: str, MsgType: type, values: list):
        super().__init__('subscriber')
        self.subscriber = self.create_subscription(MsgType, topic, self.sub_callback, qos_profile=qos_profile_sensor_data)
        self.values = values

    def sub_callback(self, msg):
        self.get_logger().info('Receiving: "%s"' % msg.data)
        self.values.append(msg.data)


class RosNode():
    def __init__(self, pub_topic: str, topic_msg_map: Dict[str, type], pub_rate_sec: float):
        rclpy.init()
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(PubNode(pub_topic, 10, pub_rate_sec))

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
        self.executor.spin()

    def stop(self):
        self.executor.shutdown()



def main():
    pass


if __name__ == '__main__':
    main()
