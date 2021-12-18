from app import settings
from app.subscription_repository import SubscriptionRepository
from app.subscription_system import Channel, OutputCollector, Subscriber

settings.TEST_MODE = True
dummy_repository = SubscriptionRepository.instance()
dummy_repository.truncate_table()
output_collector = OutputCollector()


def test_no_subscriber_publish_video() -> None:
    channel = Channel("MrBeast", output_collector)
    channel.notify_subscribers()
    assert output_collector.read_output() == "Notifying subscribers of MrBeast:\n"
    dummy_repository.truncate_table()


def test_subscribe() -> None:
    channel = Channel("MrBeast", output_collector)
    channel.subscribe(Subscriber("Jake", output_collector))
    assert output_collector.read_output() == "Jake subscribed to MrBeast\n"
    dummy_repository.truncate_table()


def test_multiple_subscription_simultaneously() -> None:
    channel = Channel("MrBeast", output_collector)
    channel.subscribe(Subscriber("Jake", output_collector))
    channel.subscribe(Subscriber("Alice", output_collector))
    channel.subscribe(Subscriber("James", output_collector))
    assert output_collector.read_output() == (
        "Jake subscribed to MrBeast\n"
        "Alice subscribed to MrBeast\n"
        "James subscribed to MrBeast\n"
    )

    dummy_repository.truncate_table()


def test_publish_video_with_subscribers() -> None:
    channel = Channel("MrBeast", output_collector)
    channel.subscribe(Subscriber("Jake", output_collector))
    channel.subscribe(Subscriber("James", output_collector))
    output_collector.read_output()
    channel.notify_subscribers()
    assert (
        output_collector.read_output() == "Notifying subscribers of MrBeast:\n"
        "\tJake\n"
        "\tJames\n"
    )
    dummy_repository.truncate_table()
