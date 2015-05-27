import os

from locust import HttpLocust, TaskSet

from rss import RSSTasks
from courses import CourseTasks
from instructors import InstructorTasks
from search import SearchTasks
from static import StaticTasks


class MarketingTest(TaskSet):

    tasks = {
        RSSTasks: 50,
        CourseTasks: 50,
        InstructorTasks: 50,
        SearchTasks: 50,
        StaticTasks: 50
    }


class MarketingLocust(HttpLocust):

    task_set = MarketingTest
    min_wait = 3 * 1000
    max_wait = 5 * 1000


