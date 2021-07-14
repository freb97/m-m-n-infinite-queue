import matplotlib.pyplot as plt
import numpy as np
import queue
from queueing import task
from queueing import server


class Simulator(object):
    """
    Class representation of a simulator.

    Attributes
    ----------
    total_time : int
        The total time the simulation runs for.
    total_tasks : int
        The number of tasks in the simulation.
    arrival_rate : int
        The average arrival rate of the tasks.
    service_rate : int
        The average service rate of the tasks.
    server_count : int
        The number of servers in the simulation.
    tasks : queue.Queue
        The queue of task objects in the simulation.
    tasks_waiting : queue.Queue
        The queue of arrived task objects in the simulation waiting for a free server.
    servers : server.Server[]
        All server objects in the simulation.
    arrival_times : int[]
        All arrival times in the simulation, sorted.
    service_times : int[]
        All service times in the simulation, unsorted.
    """

    def __init__(self, total_time, arrival_rate, service_rate, server_count):
        """
        Class constructor.

        Parameters
        ----------
        total_time : int
            The total time the simulation runs for.
        arrival_rate : int
            The average arrival rate of the tasks.
        service_rate : int
            The average service rate of the tasks.
        server_count : int
            The number of servers in the simulation.
        """

        self.total_time = total_time * 60 * 60
        self.total_tasks = total_time * arrival_rate
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.server_count = server_count

        self.tasks = queue.Queue()
        self.tasks_waiting = queue.Queue()

        self.servers = []

        self.arrival_times = []
        self.service_times = []

    def prepare(self):
        """
        Prepares the simulation.
        """

        # Create servers
        for i in range(self.server_count):
            self.servers.append(server.Server())

        # Create arrival times and service times
        for i in range(self.total_tasks):
            self.arrival_times.append(int(np.random.exponential(1 / self.arrival_rate) * 60 * 60 * 2))
            self.service_times.append(int(np.random.exponential(1 / self.service_rate) * 60 * 60))

        self.arrival_times.sort()

        # Create tasks
        for i in range(self.total_tasks):
            arrival_time = self.arrival_times[i]
            service_time = self.service_times[i]

            self.tasks.put(task.Task(arrival_time, service_time))

    def run(self):
        """
        Runs the simulation.
        """

        for current_time in range(self.total_time):

            # Check for arriving tasks
            for arrival_time in self.arrival_times:
                if current_time == arrival_time:
                    # Task arrived, add to waiting tasks
                    current_task = self.tasks.get_nowait()
                    current_task.arrival_time = arrival_time

                    self.tasks_waiting.put(current_task)

            # Check for free servers
            for current_server in self.servers:
                if not current_server.is_busy:
                    try:
                        # Server is not busy, get next waiting task
                        current_task = self.tasks_waiting.get_nowait()
                        current_task.start(current_time)

                        current_server.add_task(current_task)
                    except queue.Empty:
                        pass

                # Update all servers
                current_server.update(current_time)

    def analyze(self):
        """
        Analyzes the simulation.
        """

        total_finished_tasks = 0
        for current_server in self.servers:
            total_finished_tasks += current_server.task_count

        print("Total tasks: " + str(self.total_tasks))
        print("Tasks finished: " + str(total_finished_tasks))


def main():
    # Quantity of incoming tasks per hour
    arrival_rate = 40

    # Quantity of tasks per hour a server can handle
    service_rate = 10

    # Total simulation time in hours
    total_time = 10

    # Total number of servers in the simulation
    server_count = 4

    # Create and prepare simulation
    simulator = Simulator(total_time, arrival_rate, service_rate, server_count)
    simulator.prepare()

    # Run simulation
    simulator.run()

    # Analyze the simulation
    simulator.analyze()


if __name__ == "__main__":
    main()
