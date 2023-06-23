"""
This file is used to generate sensor data using gazebo.
"""

from world_generation import generate_world, read_file, generate_tiles, generate_objects
import subprocess
from threading import Thread, Event
import time


def create_world():
    """Creates a world with some objects inside."""

    generate_world(
        main_file="gazebo_templates/main_base.sdf",
        output_path="gazebo_generated/generated_world.sdf",
        replace_map={
            "[[ROBOT]]": read_file("gazebo_templates/stackedRobot.sdf"),
            "[[TILES]]": generate_tiles("gazebo_templates/tile_base.sdf"),
            "[[CYLINDERS]]": generate_objects("gazebo_templates/cylinder_base.sdf")
        },
    )


def exec_command(command: str):
    output = subprocess.run(command.split(" "), capture_output=True)
    print(output.stdout)


def run_ros2_node(shared_event: Event):
    while True:
        i = 0
        shared_event.set()
        while shared_event.is_set():
            time.sleep(1)
            i += 1
        print("node:", i)


def main():
    shared_event = Event()

    thread_ros2 = Thread(target=run_ros2_node, args=(shared_event,))
    thread_ros2.start()

    NUM_RUNS = 10
    for _ in range(NUM_RUNS):
        shared_event.wait()

        #create_world()
        exec_command("sleep 5")
        shared_event.clear()

    thread_ros2.join()

if __name__ == "__main__":
    main()
