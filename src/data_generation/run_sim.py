"""
This file is used to generate sensor data using gazebo.
"""

from world_generation import generate_world, read_file, generate_smoke, generate_objects
import subprocess
from threading import Thread, Event
from ros2 import RosNode, TopicMapping


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


def run_sim(main_file: str, output_path: str, replace_map: dict[str, str], 
    num_sims: int, step_size: float, duration_sec: float, sensor_topics: list[TopicMapping]
):
    num_iter = int(duration_sec / step_size)
    replace_map["[[STEP_SIZE]]"] = str(step_size)

    shared_event = Event()
    stop_event = Event()

    thread_bridge = Thread(target=run_bridge, args=(sensor_topics,))
    thread_bridge.start()

    thread_ros2 = Thread(target=run_ros2_node, args=(sensor_topics, shared_event, stop_event))
    thread_ros2.start()

    for _ in range(num_sims):
        shared_event.wait()

        print("Generating world ... ", end="", flush=True)
        generate_world(
            main_file=main_file,
            output_path=output_path,
            replace_map=replace_map,
        )
        print("done", flush=True)

        print("Running simulation ... ", end="", flush=True)
        exec_command(f"ign gazebo -s -r --iterations {num_iter} {output_path}")
        print("done", flush=True)

        shared_event.clear()

    stop_event.set()
    thread_ros2.join()


def main():
    run_sim(
        num_sims=10,
        step_size=0.1,
        duration_sec=10,
        sensor_topics=[
            # Source for mappings: https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_bridge
            TopicMapping("/lidar", "gz.msgs.LaserScan", "sensor_msgs/msg/LaserScan"),
            TopicMapping("/lidar/points", "gz.msgs.PointCloudPacked", "sensor_msgs/msg/PointCloud2"),
            TopicMapping("/model/robot/odometry", "gz.msgs.Odometry", "nav_msgs/msg/Odometry"),
            TopicMapping("/model/robot/tf", "gz.msgs.Pose_V", "geometry_msgs/msg/PoseArray"),
        ],
        main_file="gazebo_templates/main_base.sdf",
        output_path="gazebo_generated/generated_world.sdf",
        replace_map={
            "[[TILES]]": "",
            "[[CYLINDERS]]": generate_objects("gazebo_templates/cylinder_base.sdf"),
            "[[ROBOT]]": read_file("gazebo_templates/robot_stacked_drive.sdf"),
            "[[SMOKE]]": generate_smoke("gazebo_templates/fogemitter.sdf"),
        },
    )


if __name__ == "__main__":
    main()
