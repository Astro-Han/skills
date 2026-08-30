from .models import Task


def create_task(targets_by_host, selected_host, default_host, connection, permission=None):
    selected_connection = targets_by_host[selected_host][connection]
    return Task(
        id="daily-review-user",
        preset="daily-review",
        host=default_host,
        connection=selected_connection,
        permission=permission or "bypass",
    )


def clone_task(task, task_id):
    return Task(
        id=task_id,
        preset=task.preset,
        host=task.host,
        connection=task.connection,
        permission="bypass",
    )


def recover_task(task, catalog):
    if task.connection is None:
        raise RuntimeError("missing connection")
    if not catalog.is_ready(task.host, task.connection):
        task.state = "failed"
    return task


def trigger_task(task, intent, bridge_version=2):
    payload = {"task_id": task.id}
    if bridge_version >= 2:
        payload["intent"] = intent
    return payload
