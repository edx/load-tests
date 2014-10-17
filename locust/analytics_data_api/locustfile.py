"""
Load tests for the analytics data API.

The API key should be passed as an environment variable when running locust. See the example below.

API_KEY="secret" locust --host="https://api.example.org"
"""

import os
import random
from locust import HttpLocust, TaskSet, task

API_KEY = os.environ['API_KEY']

# TODO Develop a better list of courses with a wider range of data
COURSES = ['edX/DemoX/Demo_Course', 'LinuxFoundationX/LFS101x/2T2014', 'ANUx/ANU-ASTRO2x/2T2014']


class UserBehavior(TaskSet):
    def on_start(self):
        self.client.headers = {
            'Authorization': 'Token {}'.format(API_KEY)
        }

    def get_course_path(self, course_id=None, path=None):
        course_id = course_id or random.choice(COURSES)
        path = path or ''

        self.client.get("/courses/{0}/{1}".format(course_id, path))

    @task
    def course_enrollment(self):
        self.get_course_path(path='enrollment/')

    @task
    def course_enrollment_location(self):
        self.get_course_path(path='enrollment/location/')

    @task
    def course_activity(self):
        self.get_course_path(path='activity/')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
