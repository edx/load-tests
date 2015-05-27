import json
import config

from locust import task, TaskSet
from marketing import MarketingTasks

INSTRUCTOR_ID = '4306'


class InstructorTasks(MarketingTasks):
    """Locust tests related to the viewing of instructor details."""

    @task
    def instructor_search(self):
        """Simulate the searching of all courses by a single instructor."""

        get_data = {'instructor': INSTRUCTOR_ID, 'display': 'teaser'}
        self.get('/api/catalog/v2/courses', data=json.dumps(get_data))

    def instructor_view(self):
        """Simulate the viewing of instructor information."""

        self.get('/api/instructor/v1/node/' + INSTRUCTOR_ID)


