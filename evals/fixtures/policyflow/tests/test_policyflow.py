import unittest

from policyflow.intake import create_bucket_delivery, create_email_delivery


class PolicyFlowTests(unittest.TestCase):
    def test_surrounding_whitespace_is_removed(self):
        email = create_email_delivery("e1", " a@example.com ", " Alice ")
        bucket = create_bucket_delivery("b1", " Bucket-A ", " Reports ")
        self.assertEqual(email.destination, "a@example.com")
        self.assertEqual(bucket.destination, "bucket-a")


if __name__ == "__main__":
    unittest.main()
