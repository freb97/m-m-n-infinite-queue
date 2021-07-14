class Task(object):
    """
    Class representation of a task.

    Attributes
    ----------
    arrival_time : int
        The time in seconds from the start time when the task arrives in the simulation.
    service_time : int
        The time in seconds it takes to solve this particular task.
    retention_time : int
        The time it took from the arrival in the simulation to finishing the task.
    start_time : int
        The time in seconds from the start time when the task was started.
    end_time : int
        The time in seconds from the start time when the task has ended.
    """

    def __init__(self, arrival_time, service_time):
        """
        Class constructor.

        Parameters
        ----------
        arrival_time : int
            The time in seconds from the start time when the task arrives in the simulation.
        service_time : int
            The time in seconds it takes to solve this particular task.
        """

        self.arrival_time = arrival_time
        self.service_time = service_time

        self.retention_time = 0
        self.start_time = 0
        self.end_time = 0

    def start(self, current_time):
        """
        Starts the task.

        Parameters
        ----------
        current_time : int
            The current time in seconds from the start time.
        """

        self.start_time = current_time
        self.end_time = current_time + self.service_time
        self.retention_time = current_time - self.arrival_time + self.service_time
