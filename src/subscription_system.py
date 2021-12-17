from abc import ABC, abstractmethod
from typing import List

from src.subscription_repository import SubscriptionRepository


class OutputCollector:

    def __init__(self) -> None:
        self._output = ""

    def append_output(self, partial_output: str) -> None:
        self._output += partial_output

    def read_output(self) -> str:
        tmp = self._output
        self._output = ''
        return tmp


class Subject(ABC):

    @abstractmethod
    def attach(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class Observer(ABC):

    def __init__(self, name: str) -> None:
        self.name: str = name

    @abstractmethod
    def update(self, ) -> None:
        pass


class Subscriber(Observer):

    def __init__(self, name: str, output_stream: OutputCollector) -> None:
        super().__init__(name)
        self._output_stream = output_stream

    def update(self) -> None:
        self._output_stream.append_output(f'\t{self.name}\n')


class Channel(Subject):

    def __init__(self, name: str, output_stream: OutputCollector) -> None:
        self._name: str = name
        self._output_stream = output_stream
        self._subscribers: List[Observer] = []
        self._subscription_repository = SubscriptionRepository()
        self._init_mode = True
        persistent_subscribers = self._subscription_repository.get_channel_subscribers(self._name)
        for subscriber in persistent_subscribers:
            self.attach(Subscriber(subscriber, self._output_stream))
        self._init_mode = False

    def attach(self, observer: Observer) -> None:
        if not self._init_mode:
            self._subscription_repository.add_subscription(self._name, observer.name)
            self._output_stream.append_output(f'{observer.name} subscribed to {self._name}\n')
        self._subscribers.append(observer)

    def notify(self) -> None:
        self._output_stream.append_output(f'Notifying subscribers of {self._name}:\n')
        for observer in self._subscribers:
            observer.update()


class SubscriptionSystem(OutputCollector):

    def __init__(self) -> None:
        super().__init__()
        self._channels: dict[str, Channel] = {}

    def subscribe(self, subscriber: str, channel_name: str) -> None:
        self._check_channel(channel_name)
        self._channels[channel_name].attach(Subscriber(subscriber, self))
        print(self.read_output())

    def published_video_hook(self, channel_name: str) -> None:
        self._check_channel(channel_name)
        self._channels[channel_name].notify()
        print(self.read_output())

    def _check_channel(self, channel_name: str) -> None:
        if channel_name not in self._channels:
            self._channels[channel_name] = Channel(channel_name, self)
