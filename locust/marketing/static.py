import json
import config

from locust import task, TaskSet
from marketing import MarketingTasks

INSTRUCTOR_ID = '4306'


class StaticTasks(MarketingTasks):

    """Locust tests related to the viewing of static pages."""

    @task
    def homepage(self):
        """Simulate the viewing of the homepage."""

        self.get('/')

    def schools(self):
        """Simulate the viewing of a school's page."""

        self.get('/school/edx')


