import json
import config
import time
import csv

from random import randint
from locust import task, TaskSet
from marketing import MarketingTasks

SEARCH_TERM = 'math'

class SearchTasks(MarketingTasks):

    """Locust tests related to searching."""

    def on_start(self):
        csv_r = csv.reader(open('search_terms.csv', 'rb'))
        search_terms = csv_r.next()
        rand_index = randint(0, len(search_terms) - 1)
        SEARCH_TERM = search_terms[rand_index]
           
        
    def character_search(self, url):
        """Simulates a search by typing the search term."""

        for i in xrange(0, len(SEARCH_TERM)):
            term = SEARCH_TERM[0:i]
            get_data = {'query': term}
            self.get(url, data=json.dumps(get_data))
            time.sleep(0.1)

    @task
    def search(self):
        """Simulate the listing of all courses via the Search API."""

        self.get('/search/api/all')

    @task
    def search_type_course(self):
        """Simulate the character entry for course search."""

        self.character_search('/customizable_search/bundle/course')

    @task
    def search_type_subject(self):
        """Simulate the character entry for subject search."""

        self.character_search('/customizable_search/bundle/subject')

    @task
    def search_type_school(self):
        """Simulate the character entry for school search."""

        self.character_search('/customizable_search/bundle/school')

    @task
    def search_type_level(self):
        """Simulate the character entry for level search."""

        self.character_search('/customizable_search/bundle/level')

    @task
    def search_type_lang(self):
        """Simulate the character entry for language search."""

        self.character_search('/api/languages/v1/list')


