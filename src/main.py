from src.cmd_parser import get_cmd_type, CommandType, parse_publish_video_cmd, parse_subscribe_cmd
from src.subscription_system import SubscriptionSystem

subscription_system = SubscriptionSystem()

while True:
    cmd = input(">>> ").strip()
    try:
        cmd_type = get_cmd_type(cmd)
        if cmd_type == CommandType.PUBLISH_VIDEO:
            channel = parse_publish_video_cmd(cmd)
            subscription_system.published_video_hook(channel)
        elif cmd_type == CommandType.SUBSCRIBE:
            subscriber, channel = parse_subscribe_cmd(cmd)
            subscription_system.subscribe(subscriber, channel)
        else:
            raise Exception('Unknown cmd type!')
    except ValueError:
        print('Invalid cmd format, try again.')
    except Exception as e:
        print(f'Unexpected error occurred: {e}')
