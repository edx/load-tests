import json
import config

from locust import task, TaskSet
from marketing import MarketingTasks

COURSE_ID = 'edX/DemoX.1/2014'

class CourseTasks(MarketingTasks):
    """Locust tests related to course viewing."""

    @task
    def view_course_details(self):
        """Simulate the retrieval of the course feed using (API v1)."""

        self.get('/api/catalog/v2/courses/' + COURSE_ID)


