def export_subscription(subscription):
    return {
        "id": subscription.id,
        "state": subscription.state,
    }
