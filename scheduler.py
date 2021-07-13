import matplotlib.pyplot as plot
import numpy as np
import queue
from queueing import task
from queueing import server


class Simulator(object):
    def __init__(self, total_time, arrival_rate, service_rate, server_count):
        self.total_time = total_time
        self.total_tasks = total_time * arrival_rate
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.server_count = server_count

        self.tasks = queue.Queue()
        self.servers = []

        for i in range(server_count):
            self.servers.append(server.Server([], self.total_time * 60 * 60))

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

            self.tasks.put(task.Task(arrival_time, service_time))

    def run(self):
        for current_time in range(self.total_time * 60 * 60):
            tasks_waiting = []

            for arrival_time in self.arrival_times:
                if current_time == arrival_time:
                    tasks_waiting.append(self.tasks.get())

                    self.arrival_times.remove(arrival_time)

            for current_task in tasks_waiting:
                for current_server in self.servers:
                    if not current_server.is_busy:
                        current_server.add_task(current_task)

                        tasks_waiting.remove(current_task)

            current_time += 1


def main():
    # Quantity of incoming tasks per hour
    arrival_rate = 100

    # Quantity of tasks per hour a server can handle
    service_rate = 10

    # Total simulation time in hours
    total_time = 10

    # Total number of servers in the simulations
    server_count = 4

    # Create and prepare simulation
    simulator = Simulator(total_time, arrival_rate, service_rate, server_count)
    simulator.prepare()

    # Run simulation
    simulator.run()


if __name__ == "__main__":
    main()
