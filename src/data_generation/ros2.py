import rclpy
from threading import Event
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
from dataclasses import dataclass
import pickle


@dataclass
class TopicMapping:
    topic: str
    ros_type: str
    gz_type: str

    def __init__(self, topic: str, gz_type: str, ros_type: str):
        self.topic = topic
        self.gz_type = gz_type
        self.ros_type = ros_type

    def get_class(self) -> type:
        """Imports and creates a python class from a string of type: module/path/Class"""
        parts = self.ros_type.split("/")
        module_path = ".".join(parts[:-1])
        i = __import__(module_path, fromlist=parts[-1])
        return getattr(i, parts[-1])


class PubNode(Node):
    def __init__(self, topic: str, publish_value: float=10, publish_rate_sec: float=1):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(Twist, topic, 10)
        self.timer = self.create_timer(publish_rate_sec, self.timer_callback)
        self.publish_value = publish_value

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = float(self.publish_value)
        msg.angular.z = float(0)

        self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.linear)


class SubNode(Node):
    def __init__(self, topic: str, MsgType: type, values: list):
        super().__init__('subscriber')
        self.subscriber = self.create_subscription(MsgType, topic, self.sub_callback, qos_profile=qos_profile_sensor_data)
        self.values = values

    def sub_callback(self, msg):
        #self.get_logger().info('Receiving: "%s"' % msg)
        self.values.append(msg)


class RosNode():
    def __init__(self, pub_topic: str, topic_msg_map: list[TopicMapping], pub_rate_sec: float, save_event: Event|None=None, stop_event: Event|None=None):
        rclpy.init()
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(PubNode(pub_topic, 0.5, pub_rate_sec))
        self.save_event = save_event if save_event is not None else Event();
        self.stop_event = stop_event if stop_event is not None else Event();

        self.vals_map = {}
        for topic_mapping in topic_msg_map:
            self.vals_map[topic_mapping.topic] = []
            self.executor.add_node(SubNode(
                topic=topic_mapping.topic, 
                MsgType=topic_mapping.get_class(), 
                values=self.vals_map[topic_mapping.topic]
            ))

    def save_data(self):
        print("Saving to file ... ", end="", flush=True)
        vals_pickle = pickle.dumps(self.vals_map)
        with open("data/data.pickle", "wb") as f:
            f.write(vals_pickle)
        print("done", flush=True)

        for vals in self.vals_map.values():
            vals = []

        print(self.vals_map, flush=True)

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
