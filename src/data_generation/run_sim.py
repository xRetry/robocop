"""
This file is used to generate sensor data using gazebo.
"""

from world_generation import WorldGen, read_file, generate_smoke, generate_objects
import subprocess
from threading import Thread, Event
from ros2 import RosNode, TopicMapping

class SimExecutor:
    world_gen: WorldGen
    num_sims: int
    duration_sec: float
    step_size: float
    sensor_topics: list[TopicMapping]

    def __init__(self, world_gen: WorldGen, num_sims: int, duration_sec: float, step_size: float) -> None:
        self.world_gen = world_gen
        self.num_sims = num_sims
        self.duration_sec = duration_sec
        self.step_size = step_size
        self.sensor_topics = []

    def add_sensor(self, topic: str, gazebo_msg: str, ros_msg: str):
        self.sensor_topics.append(TopicMapping(topic, gazebo_msg, ros_msg))
        return self

    def run(self):
        num_iter = int(self.duration_sec / self.step_size)
        self.world_gen.replace("[[STEP_SIZE]]", str(self.step_size))

        shared_event = Event()
        stop_event = Event()

        thread_bridge = Thread(target=run_bridge, args=(self.sensor_topics,))
        thread_bridge.start()

        thread_ros2 = Thread(target=run_ros2_node, args=(self.sensor_topics, shared_event, stop_event))
        thread_ros2.start()

        for _ in range(self.num_sims):
            shared_event.wait()

            print("Generating world ... ", end="", flush=True)
            next(self.world_gen)
            print("done", flush=True)

            print("Running simulation ... ", end="", flush=True)
            exec_command(f"ign gazebo -s -r --iterations {num_iter} {self.world_gen.output_path}")
            print("done", flush=True)

            shared_event.clear()

        stop_event.set()
        thread_ros2.join()


def exec_command(command: str):
    output = subprocess.run(command.split(" "), capture_output=True)


def run_bridge(sensor_topics: list[TopicMapping]):
    cmd = "ros2 run ros_gz_bridge parameter_bridge"
    for topic_map in sensor_topics:
        cmd += f" {topic_map.topic}@{topic_map.ros_type}[{topic_map.gz_type}"

    exec_command(cmd)


def run_ros2_node(sensor_topics: list[TopicMapping], shared_event: Event, stop_event: Event):
    pub_topic = "/cmd_vel"
    node = RosNode(
        pub_topic=pub_topic, 
        topic_msg_map=sensor_topics, 
        pub_rate_sec=1, 
        save_event=shared_event,
        stop_event=stop_event,
    )
    node.start()


def main():
    world_gen = WorldGen(
        main_file="gazebo_templates/main_base.sdf",
        output_path="gazebo_generated/generated_world.sdf",
    )
    (world_gen.replace("[[TILES]]", "") 
        .replace("[[CYLINDERS]]", generate_objects("gazebo_templates/cylinder_base.sdf"))
        .replace("[[ROBOT]]", read_file("gazebo_templates/robot_stacked_drive.sdf"))
        .replace("[[SMOKE]]", generate_smoke("gazebo_templates/fogemitter.sdf"))
    )

    executor = (SimExecutor(
        world_gen=world_gen,
        num_sims=10,
        step_size=0.1,
        duration_sec=5
        )
        .add_sensor("/lidar", "gz.msgs.LaserScan", "sensor_msgs/msg/LaserScan")
        .add_sensor("/lidar/points", "gz.msgs.PointCloudPacked", "sensor_msgs/msg/PointCloud2")
        .add_sensor("/model/robot/odometry", "gz.msgs.Odometry", "nav_msgs/msg/Odometry")
        .add_sensor("/model/robot/tf", "gz.msgs.Pose_V", "geometry_msgs/msg/PoseArray")
    )
    executor.run()


if __name__ == "__main__":
    main()
