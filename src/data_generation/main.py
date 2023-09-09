"""
This file is used to generate sensor data using gazebo.
"""

from world_generation import WorldGen, read_file, generate_smoke, generate_objects
from ros2 import RosCollector
from sim_executor import SimExecutor


def main():
    ros_collector = (RosCollector(
        pub_topic="/cmd_vel", 
        pub_rate_sec=1, 
    )
        .add_sensor("/lidar", "gz.msgs.LaserScan", "sensor_msgs/msg/LaserScan")
        .add_sensor("/lidar/points", "gz.msgs.PointCloudPacked", "sensor_msgs/msg/PointCloud2")
        .add_sensor("/model/robot/odometry", "gz.msgs.Odometry", "nav_msgs/msg/Odometry")
        .add_sensor("/model/robot/tf", "gz.msgs.Pose_V", "geometry_msgs/msg/PoseArray")
    )

    step_size = 0.1
    world_gen = WorldGen(
        main_file="gazebo_templates/main_base.sdf",
        output_path="gazebo_generated/generated_world.sdf",
        replace_map={
            "[[TILES]]": "",
            "[[CYLINDERS]]": lambda: generate_objects("gazebo_templates/cylinder_base.sdf"),
            "[[ROBOT]]": lambda: read_file("gazebo_templates/robot_stacked_drive.sdf"),
            "[[SMOKE]]": lambda: generate_smoke("gazebo_templates/fogemitter.sdf"),
            "[[STEP_SIZE]]": str(step_size)
        }
    )

    executor = SimExecutor(
        world_gen=world_gen,
        collector=ros_collector,
        num_sims=3,
        step_size=step_size,
        duration_sec=3
    )
    executor.run()


if __name__ == "__main__":
    main()
