import unittest

from digestflow.execution import create_task, trigger_task
from digestflow.models import Session, TargetCatalog, Task
from digestflow.projection import activity_total, report_rows


class DigestFlowTests(unittest.TestCase):
    def test_current_report_is_visible(self):
        session = Session(
            id="s1",
            task_id="task-1",
            preset="daily-review",
            root_id="s1",
            revision=1,
            state="complete",
            artifact="report",
        )
        task = Task("task-1", "daily-review", "host-a", "conn-a", "ask")
        self.assertEqual(report_rows([session], task), [session])

    def test_task_uses_requested_connection(self):
        task = create_task({"host-a": {"primary": "conn-a"}}, "host-a", "host-a", "primary")
        self.assertEqual(task.connection, "conn-a")

    def test_new_bridge_keeps_intent(self):
        task = create_task({"host-a": {"primary": "conn-a"}}, "host-a", "host-a", "primary")
        self.assertEqual(trigger_task(task, "last-7-days")["intent"], "last-7-days")

    def test_empty_activity_is_zero(self):
        self.assertEqual(activity_total([]), 0)


if __name__ == "__main__":
    unittest.main()
