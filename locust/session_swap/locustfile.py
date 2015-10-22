from locust import HttpLocust, TaskSet, task
import os
import random


BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (
        os.environ['BASIC_AUTH_USER'],
        os.environ['BASIC_AUTH_PASSWORD']
    )
SESSION_IDS = os.environ['SESSION_IDS'].split(',')


class Events(TaskSet):

    @task
    def show_transcript_event(self):
        params = '/event?'\
                 'event_type=show_transcript'\
                 '&event=%7B%22id%22%3A%22i4x-BerkeleyX-Stat2_1x-video-58424ad2f75048798b4480aa699cc215%22%2C%22' \
                 'currentTime%22%3A0%2C%22code%22%3A%22iOOYGgLADj8%22%7D' \
                 '&page=https%3A%2F%2Fcourses.edx.org%2Fcourses%2FBerkeleyX%2FStat2.1x%2F2013_Spring%' \
                 '2Fcourseware%2Fd4ff35dabfe64ed5b1f1807eb0292c73%2Fbd343b7dcb2c4817bd1992b0cef66ff4%2F'

        auth = None
        if BASIC_AUTH_CREDENTIALS:
            auth = BASIC_AUTH_CREDENTIALS
        self.client.get(params, cookies={'sessionid': self.locust.session_id}, auth=auth)


class WebsiteUser(HttpLocust):
    task_set = Events
    min_wait=100
    max_wait=1000

    def __init__(self):
        super(WebsiteUser, self).__init__()
        self.session_id = random.choice(SESSION_IDS)
