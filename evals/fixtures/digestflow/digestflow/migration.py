from .models import Session, Task


def migrate_legacy(snapshot, catalog, tasks, sessions):
    if snapshot["version"] != 2:
        raise ValueError("unsupported legacy schema")

    for report in snapshot["reports"]:
        sessions.append(
            Session(
                id="legacy-{}".format(report["id"]),
                task_id="daily-review-pending",
                preset="daily-review",
                root_id=report["id"],
                revision=1,
                state="complete",
                artifact=report["body"],
            )
        )

    connection = snapshot.get("connection")
    if snapshot["enabled"] and not catalog.is_ready(snapshot["host"], connection):
        return False

    tasks.append(
        Task(
            id="daily-review-{}".format(len(tasks) + 1),
            preset="daily-review",
            host=snapshot["host"],
            connection=connection,
            permission=snapshot.get("permission", "bypass"),
        )
    )
    return True
