from enum import Enum
from typing import Tuple


class CommandType(Enum):
    SUBSCRIBE = 1
    PUBLISH_VIDEO = 2


def get_cmd_type(cmd: str) -> CommandType:
    if cmd.startswith('subscribe <'):
        return CommandType.SUBSCRIBE
    elif cmd.startswith('publish video on <'):
        return CommandType.PUBLISH_VIDEO
    else:
        raise ValueError()


def parse_subscribe_cmd(cmd: str) -> Tuple[str, str]:
    if cmd.startswith('subscribe <'):
        cmd = cmd[len('subscribe <'):]
    else:
        raise ValueError()

    subscriber_end_index = cmd.index('> to <')

    if subscriber_end_index != -1:
        subscriber = cmd[:subscriber_end_index]
        cmd = cmd[len(subscriber) + len('> to <'):]
    else:
        raise ValueError()

    if cmd.endswith('>'):
        channel = cmd[:-1]
    else:
        raise ValueError()

    return subscriber, channel


def parse_publish_video_cmd(cmd: str) -> str:
    if cmd.startswith('publish video on <'):
        cmd = cmd[len('publish video on <'):]
    else:
        raise ValueError()

    if cmd.endswith('>'):
        cmd = cmd[:-1]
    else:
        raise ValueError()

    return cmd
