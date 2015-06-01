import os
import json

from locust import task

from marketing import MarketingTasks


class InstructorTasks(MarketingTasks):
    """Locust tests related to the viewing of instructor details."""

    INSTRUCTOR_ID = os.getenv('INSTRUCTOR_ID', '4306')

    @task
    def instructor_search(self):
        """Simulate the searching of all courses by a single instructor."""

        get_data = {'instructor': self.INSTRUCTOR_ID, 'display': 'teaser'}
        self.client.get('/api/catalog/v2/courses', data=json.dumps(get_data))

    @task
    def instructor_view(self):
        """Simulate the viewing of instructor information."""

        self.client.get('/api/instructor/v1/node/' + self.INSTRUCTOR_ID)
