from .models import Recipient


def canonical_email(value):
    return value.strip()


def clean_display_name(value):
    return value.strip().lower()


def create_recipient(recipient_id, email, display_name, legacy_route=None):
    return Recipient(
        recipient_id,
        canonical_email(email),
        clean_display_name(display_name),
        legacy_route,
    )


def find_recipient(recipients, email):
    return next((item for item in recipients if item.email == email.strip()), None)


def add_invitation(recipients, email, display_name):
    if any(item.email == email.strip() for item in recipients):
        return None
    recipient = create_recipient(str(len(recipients) + 1), email, display_name)
    recipients.append(recipient)
    return recipient
