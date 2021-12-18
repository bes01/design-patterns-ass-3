from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

from app.subscription_system import SubscriptionSystem


class CommandType(Enum):
    SUBSCRIBE = 1
    PUBLISH_VIDEO = 2


class CMDParser:
    @staticmethod
    def get_cmd_type(cmd: str) -> CommandType:
        if cmd.startswith("subscribe <"):
            return CommandType.SUBSCRIBE
        elif cmd.startswith("publish video on <"):
            return CommandType.PUBLISH_VIDEO
        else:
            raise ValueError()

    @staticmethod
    def parse_subscribe_cmd(cmd: str) -> Tuple[str, str]:
        if cmd.startswith("subscribe <"):
            start_index = len("subscribe <")
            cmd = cmd[start_index:]
        else:
            raise ValueError()

        subscriber_end_index = cmd.index("> to <")

        if subscriber_end_index != -1:
            subscriber = cmd[:subscriber_end_index]
            start_index = len(subscriber) + len("> to <")
            cmd = cmd[start_index:]
        else:
            raise ValueError()

        if cmd.endswith(">"):
            channel = cmd[:-1]
        else:
            raise ValueError()

        return subscriber, channel

    @staticmethod
    def parse_publish_video_cmd(cmd: str) -> str:
        if cmd.startswith("publish video on <"):
            start_index = len("publish video on <")
            cmd = cmd[start_index:]
        else:
            raise ValueError()

        if cmd.endswith(">"):
            cmd = cmd[:-1]
        else:
            raise ValueError()

        return cmd


class Command(ABC):
    def __init__(self, cmd: str, subscription_system: SubscriptionSystem):
        self._cmd = cmd
        self._subscription_system = subscription_system

    @abstractmethod
    def execute(self) -> None:
        pass


class PublishVideoCommand(Command):
    def __init__(self, cmd: str, subscription_system: SubscriptionSystem):
        super().__init__(cmd, subscription_system)

    def execute(self) -> None:
        channel = CMDParser.parse_publish_video_cmd(self._cmd)
        self._subscription_system.published_video_hook(channel)


class SubscribeCommand(Command):
    def __init__(self, cmd: str, subscription_system: SubscriptionSystem):
        super().__init__(cmd, subscription_system)

    def execute(self) -> None:
        subscriber, channel = CMDParser.parse_subscribe_cmd(self._cmd)
        self._subscription_system.subscribe(subscriber, channel)


class CLI:
    def __init__(self) -> None:
        self._subscription_system = SubscriptionSystem()

    def run_command(self, cmd: str) -> None:
        try:
            cmd_type = CMDParser.get_cmd_type(cmd)
            if cmd_type == CommandType.PUBLISH_VIDEO:
                PublishVideoCommand(cmd, self._subscription_system).execute()
            elif cmd_type == CommandType.SUBSCRIBE:
                SubscribeCommand(cmd, self._subscription_system).execute()
            else:
                raise Exception("Unknown cmd type!")
        except ValueError:
            print("Invalid cmd format, try again.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
