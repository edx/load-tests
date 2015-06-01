from locust import task, TaskSet


class MarketingTasks(TaskSet):
    """Base task class for exercising marketing-related operations."""

    @task
    def stop(self):
        """
        Supports usage as nested or top-level task set.
        """
        if self.parent != self.locust:
            self.interrupt()
