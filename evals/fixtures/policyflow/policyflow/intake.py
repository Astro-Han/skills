from .models import Delivery
from .normalization import canonical_bucket, canonical_email, clean_label


def create_email_delivery(delivery_id, email, label, legacy_route=None):
    return Delivery(
        delivery_id,
        canonical_email(email),
        clean_label(label),
        legacy_route,
    )


def find_email_delivery(deliveries, email):
    target = email.strip()
    return next((item for item in deliveries if item.destination == target), None)


def create_bucket_delivery(delivery_id, bucket, label):
    return Delivery(delivery_id, canonical_bucket(bucket), clean_label(label))
