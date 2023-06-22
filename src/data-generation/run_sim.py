"""
This file is used to generate sensor data using a robotic simulator.

The planned methodology assumes the simulator API provides the following functionality:
- Accessing the world/enviroment objects
- Placing a robot at a specific location
- Starting the simulation
- Accessing the robots sensor readings

So far, the file only contains the outline. Implementation details are missing.
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


def run_ros2_node(sim_done: Event, sim_ready: Event, node_ready: Event):
    while True:
        i = 0
        node_ready.set()
        sim_ready.wait()
        while not sim_done.is_set():
            node_ready.clear()
            time.sleep(1)
            i += 1
        print("node:", i)


# TODO: Fix deadlock :(
def main():
    sim_done = Event()
    node_ready = Event()
    sim_ready = Event()

    thread_ros2 = Thread(target=run_ros2_node, args=(sim_done, sim_ready, node_ready))
    thread_ros2.start()

    NUM_RUNS = 3
    for _ in range(NUM_RUNS):
        node_ready.wait()
        sim_done.clear()
        sim_ready.set()

        #create_world()
        exec_command("sleep 5")
        sim_ready.clear()
        sim_done.set()
        node_ready.wait()

    thread_ros2.join()

if __name__ == "__main__":
    main()
