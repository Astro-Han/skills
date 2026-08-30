def export_recipient(recipient):
    return {
        "id": recipient.id,
        "email": recipient.email,
        "display_name": recipient.display_name,
    }
