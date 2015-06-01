import json
import csv
import random

from locust import task

from marketing import MarketingTasks

# Task weights are based on the percentage of overall
# page views according to Google Analytics (05/29)

search_terms = []

with open('search_terms.csv', 'rb') as csv_file:
    csv_reader = csv.reader(csv_file)

    for row in csv_reader:
        search_terms.append(row)

class SearchTasks(MarketingTasks):
    """Locust tests related to searching."""

    def query(self, url):
        """Randomly selects a search term and passes it to the specified URL."""
        term = random.choice(search_terms)
        get_data = {'query': term}
        self.client.get(url, data=json.dumps(get_data))

    @task(5)
    def search(self):
        """Simulate the listing of all courses via the Search API."""

        self.client.get('/search/api/all')

    @task(5)
    def search_type_course(self):
        """Simulate course search."""

        self.query('/customizable_search/bundle/course')

    @task(1)
    def search_type_subject(self):
        """Simulate subject search."""

        self.query('/customizable_search/bundle/subject')

    @task(1)
    def search_type_school(self):
        """Simulate school search."""

        self.query('/customizable_search/bundle/school')

    @task(1)
    def search_type_level(self):
        """Simulate level search."""

        self.query('/customizable_search/bundle/level')

    @task(1)
    def search_type_lang(self):
        """Simulate language search."""

        self.query('/api/languages/v1/list')
