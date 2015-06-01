import os

from locust import task

from marketing import MarketingTasks


class CourseTasks(MarketingTasks):
    """Locust tests related to course viewing."""

    COURSE_ID = os.getenv('COURSE_ID', 'edX/DemoX.1/2014')

    @task
    def view_course_details(self):
        """Simulate the retrieval of the course feed using (API v1)."""
        self.client.get('/api/catalog/v2/courses/' + self.COURSE_ID)
