"""
This file is used to generate sensor data using gazebo.
"""

from world_generation import generate_world, read_file, generate_smoke, generate_objects
import subprocess
from threading import Thread, Event
from ros2 import RosNode
from sensor_msgs.msg import LaserScan, PointCloud
from nav_msgs.msg import Odometry
#from actuator_msgs.msg import 
#from geometry_msgs.msg import
#from action_msgs.msg import
#from tf2_msgs.msg import
#from tf2_geometry_msgs import Pose
#from pcl_msgs.msg import
#from diagnostic_msgs.msg import
#from visualization_msgs.msg import
#from map_msgs.msg import 


def exec_command(command: str):
    output = subprocess.run(command.split(" "), capture_output=True)
    print(output.stdout)
    ls = LaserScan()
    ls.intensities



def run_ros2_node(sensor_topics: dict[str, type], shared_event: Event, stop_event: Event):
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
    num_sims: int, step_size: float, duration_sec: float, sensor_topics: dict[str, type]
):
    num_iter = duration_sec / step_size
    replace_map["[[STEP_SIZE]]"] = str(step_size)

    shared_event = Event()
    stop_event = Event()

    thread_ros2 = Thread(target=run_ros2_node, args=(sensor_topics, shared_event, stop_event))
    thread_ros2.start()

    for _ in range(num_sims):
        shared_event.wait()

        generate_world(
            main_file=main_file,
            output_path=output_path,
            replace_map=replace_map,
        )
        exec_command(f"ign gazebo -s -r --iterations {num_iter} {output_path}")
        print('sim done')
        shared_event.clear()

    stop_event.set()
    thread_ros2.join()


def main():
    run_sim(
        num_sims=10,
        step_size=0.1,
        duration_sec=1,
        sensor_topics={
            "/lidar": LaserScan,
            "/lidar/points": PointCloud, # PointCloudPacked?
            "/model/robot/odometry": Odometry,
            # "/model/robot/tf": Pose_V?,
        }, 
        main_file="gazebo_templates/main_base.sdf",
        output_path="gazebo_generated/generated_world.sdf",
        replace_map={
            "[[STEP_SIZE]]": str(0.1),
            "[[TILES]]": "",
            "[[CYLINDERS]]": generate_objects("gazebo_templates/cylinder_base.sdf"),
            "[[ROBOT]]": read_file("gazebo_templates/robot_stacked_drive.sdf"),
            "[[SMOKE]]": generate_smoke("gazebo_templates/fogemitter.sdf"),
        },
    )


if __name__ == "__main__":
    main()
