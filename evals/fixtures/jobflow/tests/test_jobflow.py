import unittest

from jobflow.model import Job


class TestJobFlow(unittest.TestCase):
    def test_job_starts_pending(self):
        job = Job()
        self.assertEqual(job.status, "pending")
        self.assertEqual(job.history, ["pending"])

    def test_transition_changes_status(self):
        job = Job()
        job.transition("done")
        self.assertEqual(job.status, "done")

    def test_same_state_transition_returns(self):
        job = Job()
        job.transition("pending")
        self.assertEqual(job.status, "pending")


if __name__ == "__main__":
    unittest.main()
