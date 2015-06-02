from locust import task

from marketing import MarketingTasks

# Task weights are based on the percentage of overall
# page views according to Google Analytics (05/29)


class StaticTasks(MarketingTasks):
    """Locust tests related to the viewing of static pages."""

    @task(30)
    def homepage(self):
        """Simulate the viewing of the homepage."""

        self.client.get('/')

    @task(5)
    def schools(self):
        """Simulate the viewing of a school's page."""

        self.client.get('/school/edx')
