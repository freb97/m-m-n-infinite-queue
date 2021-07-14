class Server(object):
    """
    Class representation of a server.
    A server that solves tasks in this context, not a server from networking.

    Attributes
    ----------
    task : task.Task
        The current task to solve.
    is_busy : bool
        The current busy state of the server.
    idle_time : int
        The time this server spent idling.
    active_time : int
        The time this server was busy.
    task_count : int
        The number of tasks this server has finished.
    """

    def __init__(self):
        """
        Class constructor.
        """

        self.task = None
        self.is_busy = False

        self.idle_time = 0
        self.active_time = 0
        self.task_count = 0

        self.finished_tasks = []

    def update(self, current_time):
        """
        Updates the server. This is called once every second of the simulation.

        Parameters
        ----------
        current_time : int
            The current time of the simulation.
        """

        if self.is_busy:
            if current_time == self.task.end_time:
                self.finished_tasks.append(self.task)

                self.task = None
                self.task_count += 1
                self.is_busy = False
            else:
                self.active_time += 1
        else:
            self.idle_time += 1

    def add_task(self, task):
        """
        Adds a task to the server if the server is not busy.

        Parameters
        ----------
        task : task.Task
            The task to add to the server.
        """

        if self.is_busy:
            return

        self.is_busy = True
        self.task = task
