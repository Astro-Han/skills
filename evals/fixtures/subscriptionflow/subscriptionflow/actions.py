from .models import Subscription


def pause(subscription: Subscription) -> None:
    subscription.state = "paused"


def cancel_from_row(subscription: Subscription, _row: dict[str, str]) -> None:
    subscription.state = "cancelled"


def resume_after_payment(subscription: Subscription) -> None:
    subscription.state = "active"
