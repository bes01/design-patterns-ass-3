from abc import ABC, abstractmethod
from typing import List

from src.subscription_repository import SubscriptionRepository


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class Observer(ABC):
    @abstractmethod
    def update(self,) -> None:
        pass


class Subscriber(Observer):

    def __init__(self, name: str):
        self.name: str = name

    # TODO: somehow return value to test final output
    def update(self) -> None:
        print(f'\t{self.name}')


# TODO: Wrap with decorator which will print results and also serve as RELP
class Channel(Subject):

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._subscribers: List[Observer] = []
        self._subscription_repository = SubscriptionRepository.get_instance()
        persistent_subscribers = self._subscription_repository.get_channel_subscribers(self._name)
        for subscriber in persistent_subscribers:
            self.attach(Subscriber(subscriber))

    # TODO: somehow return value to test final output
    def attach(self, observer: Observer) -> None:
        self._subscribers.append(observer)

    # TODO: somehow return value to test final output
    def notify(self) -> None:
        print(f"Notifying subscribers of {self._name}:")
        for observer in self._subscribers:
            observer.update()
