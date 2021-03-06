import sqlite3
from typing import List, Optional

from app import settings


class SubscriptionRepository:
    _instance: Optional["SubscriptionRepository"] = None

    def __init__(self) -> None:
        if settings.TEST_MODE:
            db_name = settings.TEST_DB_NAME
        else:
            db_name = settings.PROD_DB_NAME
        self._datasource = sqlite3.connect(f"../db/{db_name}.db")

        cursor = self._datasource.cursor()
        cursor.execute(
            "create table if not exists subscriptions "
            "(channel TEXT NOT NULL,  subscriber TEXT NOT NULL);"
        )
        cursor.close()

    @classmethod
    def instance(cls) -> "SubscriptionRepository":
        if cls._instance is None:
            cls._instance = SubscriptionRepository()
        return cls._instance

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

    def truncate_table(self) -> None:
        cursor = self._datasource.cursor()
        cursor.execute("delete from subscriptions")
        self._datasource.commit()
        cursor.close()
