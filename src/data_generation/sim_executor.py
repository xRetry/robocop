"""
This file contains the definition of the simulation executor.
"""

import utils
from typing import Iterator
from data_collector import Collector, EventChannel
from threading import Thread


class SimExecutor:
    world_gen: Iterator[str]
    num_sims: int
    duration_sec: float
    step_size: float
    collector: Collector

    def __init__(self, world_gen: Iterator[str], collector: Collector, num_sims: int, duration_sec: float, step_size: float) -> None:
        self.world_gen = world_gen
        self.collector = collector
        self.num_sims = num_sims
        self.duration_sec = duration_sec
        self.step_size = step_size

    def run(self):
        num_iter = int(self.duration_sec / self.step_size)

        event_channel = EventChannel()
        thread_collector = Thread(target=self.collector.start, args=(event_channel,))
        thread_collector.start()

        for _ in range(self.num_sims):
            event_channel.wait_for_collector()

            print("Generating world ... ", end="", flush=True)
            try:
                out_path = next(self.world_gen)
            except StopIteration:
                print("break", flush=True)
                break
            print("done", flush=True)

            print("Running simulation ... ", end="", flush=True)
            utils.exec_command(f"ign gazebo -s -r --iterations {num_iter} {out_path}")
            print("done", flush=True)

            event_channel.set_sim_done()

        event_channel.set_shutdown()
        thread_collector.join()

