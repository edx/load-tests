"""
Load tests for the analytics events API.

Simple test to access a given video in courseware.

"""

from locust import HttpLocust, TaskSet

def get_video_event(l):
    """ Load test: Method to make call against events api (show_transcript video event). """

    params = '/event?'\
             'event_type=show_transcript'\
             'event=%7B%22id%22%3A%22i4x-BerkeleyX-Stat2_1x-video-58424ad2f75048798b4480aa699cc215%22%2C%22' \
             'currentTime%22%3A0%2C%22code%22%3A%22iOOYGgLADj8%22%7D' \
             'page=https%3A%2F%2Fcourses.edx.org%2Fcourses%2FBerkeleyX%2FStat2.1x%2F2013_Spring%' \
             '2Fcourseware%2Fd4ff35dabfe64ed5b1f1807eb0292c73%2Fbd343b7dcb2c4817bd1992b0cef66ff4%2F'

    r = l.client.get(params)

    if r.status_code != 200:
        raise Exception("Unable to grab event.")

class Events(TaskSet):
    tasks = {get_video_event:1}

    def on_start(self):
        get_video_event(self)

class WebsiteUser(HttpLocust):
    task_set = Events
    min_wait=5000
    max_wait=9000