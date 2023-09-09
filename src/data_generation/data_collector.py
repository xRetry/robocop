from threading import Event
import abc

class EventChannel:
    main_event: Event
    stop_event: Event

    def __init__(self):
        self.main_event = Event()
        self.stop_event = Event()
        
    def wait_for_collector(self):
        self.main_event.wait()

    def collector_ready(self) -> None:
        self.main_event.set()
        
    def set_sim_done(self) -> None:
        self.main_event.clear()

    def sim_done(self) -> bool:
        return not self.main_event.is_set() or self.stop_event.is_set()
    
    def set_shutdown(self) -> None:
        self.stop_event.set()
        
    def shutdown(self) -> bool:
        return self.stop_event.isSet()


class Collector(abc.ABC):
    @abc.abstractmethod
    def start(self, event_channel: EventChannel) -> None:
        pass

