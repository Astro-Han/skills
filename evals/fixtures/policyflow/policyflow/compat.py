def export_delivery(delivery):
    return {
        "id": delivery.id,
        "destination": delivery.destination,
        "label": delivery.label,
    }
