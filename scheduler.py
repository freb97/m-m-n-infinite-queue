import this

import numpy as np


class Task:
    def __init__(self, task_id, arrival_time, service_time):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.service_time = service_time


class Scheduler:
    def __init__(self, total_time, tasks_per_hour, service_rate):
        self.task_count = tasks_per_hour * total_time
        self.arrival_rate = 0.05 * tasks_per_hour
        self.tasks_per_hour = tasks_per_hour
        self.total_time = total_time * 3600
        self.service_rate = service_rate
        self.current_time = 0
        self.tasks = self.generate_tasks()

    def generate_tasks(self):
        task_id = 1

        tasks = {}

        for i in range(self.task_count):
            arrival_time = self.calculate_arrival_time(self.arrival_rate)
            service_time = self.calculate_service_time(self.service_rate)

            tasks[i] = Task(task_id, arrival_time, service_time)

            task_id += 1

        return tasks

    @staticmethod
    def calculate_service_time(service_rate):
        return np.random.exponential(service_rate)

    @staticmethod
    def calculate_arrival_time(arrival_rate):
        return np.random.exponential(arrival_rate)


def main():
    # 10 hours, 30 tasks per hour, 0.01 hours per task
    scheduler = Scheduler(10, 30, 0.01)


if __name__ == "__main__":
    main()
