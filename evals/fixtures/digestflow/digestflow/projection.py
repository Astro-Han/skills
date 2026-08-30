def report_rows(sessions, current_task):
    return [
        session
        for session in sessions
        if session.task_id == current_task.id and session.artifact is not None
    ]


def activity_total(sessions):
    return sum([1 for _session in sessions])


def active_conversations(sessions):
    return len([session for session in sessions if session.state == "active"])
