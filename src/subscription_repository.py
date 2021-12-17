import sqlite3
from typing import List


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SubscriptionRepository(metaclass=SingletonMeta):
    _instance: "SubscriptionRepository" = None

    def __init__(self, db_name: str = 'on_disk') -> None:
        self._datasource = sqlite3.connect(f'db/{db_name}.db')

        cursor = self._datasource.cursor()
        cursor.execute(
            "create table if not exists subscriptions "
            "(channel TEXT NOT NULL,  subscriber TEXT NOT NULL);"
        )
        cursor.close()

    def add_subscription(self, channel: str, subscriber: str) -> None:
        cursor = self._datasource.cursor()
        cursor.execute(
            "insert into subscriptions values (?, ?);", (channel, subscriber)
        )
        self._datasource.commit()
        cursor.close()

    def get_channel_subscribers(self, channel: str) -> List[str]:
        cursor = self._datasource.cursor()
        rows = cursor.execute(
            f"select s.subscriber from subscriptions s where s.channel = '{channel}'"
        )
        subscribers = [row[0] for row in rows]
        cursor.close()
        return subscribers
