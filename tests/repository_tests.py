from app import settings
from app.subscription_repository import SubscriptionRepository

settings.TEST_MODE = True

dummy_repository = SubscriptionRepository.instance()
dummy_repository.truncate_table()


def test_no_subscriber() -> None:
    subscribers = dummy_repository.get_channel_subscribers('MrBeast')
    assert len(subscribers) == 0


def test_multiple_subscriber_addition() -> None:
    dummy_repository.add_subscription('MrBeast', 'Jake')
    dummy_repository.add_subscription('MrBeast', 'Alice')
    subscribers = dummy_repository.get_channel_subscribers('MrBeast')
    assert len(subscribers) == 2 and 'Jake' in subscribers and 'Alice' in subscribers

    dummy_repository.add_subscription('MrBeast', 'James')
    subscribers = dummy_repository.get_channel_subscribers('MrBeast')
    assert len(subscribers) == 3 and 'James' in subscribers

    dummy_repository.truncate_table()
