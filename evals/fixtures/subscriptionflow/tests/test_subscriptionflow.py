import unittest

from subscriptionflow.actions import pause
from subscriptionflow.models import Session, Subscription
from subscriptionflow.projection import active_total


class SubscriptionFlowTests(unittest.TestCase):
    def test_pause_changes_state(self):
        subscription = Subscription("s1", "active")
        pause(subscription)
        self.assertEqual(subscription.state, "paused")

    def test_active_total_counts_active_rows(self):
        sessions = [Session("a", "root-a", 1, "active")]
        self.assertEqual(active_total(sessions), 1)


if __name__ == "__main__":
    unittest.main()
