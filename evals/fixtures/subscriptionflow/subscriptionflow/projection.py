def active_rows(sessions):
    return [session for session in sessions if session.state == "active"]


def active_total(sessions):
    return len(active_rows(sessions))
