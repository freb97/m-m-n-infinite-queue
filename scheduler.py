import matplotlib.pyplot as plt
import numpy as np
import queue


class Task(object):
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time

        self.retention_time = 0
        self.start_time = 0
        self.end_time = 0

    def start(self, current_time):
        self.start_time = current_time
        self.end_time = current_time + self.service_time
        self.retention_time = current_time - self.arrival_time + self.service_time


class System(object):
    def __init__(self, tasks, total_time):
        self.tasks = tasks
        self.total_time = total_time

        self.unfinished_tasks = 0
        self.task_count = 0
        self.idle_time = 0
        self.is_busy = 0

    def run(self):
        current_task = self.tasks.get()

        for i in range(self.total_time):
            if self.is_busy and i >= current_task.end_time:
                if not self.tasks.empty():
                    current_task = self.tasks.get()
                self.is_busy = 0

            if i < current_task.arrival_time:
                if not self.is_busy:
                    self.idle_time += 1
                continue

            if self.is_busy:
                continue

            if current_task.start_time != 0:
                self.idle_time += 1
                continue

            current_task.start(i)
            # print("Arrival: " + str(current_task.arrival_time))
            # print("Start: " + str(current_task.start_time))
            # print("Retention: " + str(current_task.retention_time))
            self.task_count += 1
            self.is_busy = 1

        if current_task.end_time > self.total_time:
            self.unfinished_tasks += 1

        if not self.tasks.empty():
            self.unfinished_tasks += len(self.tasks.queue)

    def analyze(self):
        if not self.tasks.empty():
            print(str(self.unfinished_tasks) + " task(s) were not finished because the total time was reached.")

        print("Total time (in seconds): " + str(self.total_time))
        print("Task count: " + str(self.task_count))
        print("Wait time (in seconds): " + str(self.idle_time))


class Simulator(object):
    def __init__(self, total_time, arrival_rate, service_rate):
        self.total_time = total_time
        self.total_tasks = total_time * arrival_rate
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate

        self.tasks = queue.Queue()
        self.system = System([], self.total_time * 60 * 60)

        self.arrival_times = []
        self.service_times = []

    def prepare(self):
        for i in range(self.total_tasks):
            self.arrival_times.append(np.random.exponential(1 / self.arrival_rate) * 60 * 60 * self.total_time)
            self.service_times.append(np.random.exponential(1 / self.service_rate) * 60 * 60)

        self.arrival_times.sort()

        for i in range(self.total_tasks):
            arrival_time = self.arrival_times[i]
            service_time = self.service_times[i]

            self.tasks.put(Task(arrival_time, service_time))

        self.system.tasks = self.tasks

    def run(self):
        self.system.run()

    def analyze(self):
        self.system.analyze()


def main():
    # Quantity of incoming tasks per hour
    arrival_rate = 5

    # Quantity of tasks per hour the system can handle
    service_rate = 5

    # Total simulation time in hours
    total_time = 5

    # Create and prepare simulation
    simulator = Simulator(total_time, arrival_rate, service_rate)
    simulator.prepare()

    # Run simulation
    simulator.run()

    # Analyze simulation data
    simulator.analyze()


if __name__ == "__main__":
    main()
