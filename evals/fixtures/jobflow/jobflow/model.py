class Job:
    def __init__(self):
        self.status = "pending"
        self.history = ["pending"]

    def transition(self, new_status):
        self.status = new_status
