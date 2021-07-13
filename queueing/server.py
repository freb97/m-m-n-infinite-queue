class Server(object):
    def __init__(self, tasks, total_time):
        self.tasks = tasks
        self.total_time = total_time

        self.unfinished_tasks = 0
        self.task_count = 0
        self.idle_time = 0
        self.is_busy = False

    def run(self):
        if self.is_busy:
            return

        self.is_busy = True

    def add_task(self, task):
        self.tasks.append(task)
        self.unfinished_tasks += 1
