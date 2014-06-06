from locust import HttpLocust, TaskSet
import time

SERVER = 'jzoldak.m.sandbox.edx.org'
PORT = None
BASIC_AUTH_USER = 'foo'
BASIC_AUTH_PASSWORD = 'bar'
PROTOCOL = 'http'
COURSE_ID = 'edX/Open_DemoX/edx_demo_course'
TIMEOUT_MS = 10000
TOTAL_USERS = 10
RAMPUP_SEC = 60
DURATION_MS = 300000


def http_auth(self):
    pass

def auto_auth(self):
    url = '/auto_auth?course_id={}'.format(COURSE_ID)
    self.client.get(url)

def courseware(self):
    url = '/courses/{}/courseware'.format(COURSE_ID)
    self.client.get(url)

def dashboard(self):
    url = '/dashboard'
    self.client.get(url)

def info(self):
    url = '/courses/{}/info'.format(COURSE_ID)
    self.client.get(url)

def progress(self):
    url = '/courses/{}/progress'.format(COURSE_ID)
    self.client.get(url)

class StudentUser(TaskSet):
    tasks = { courseware: 825, dashboard: 125, info: 40, progress: 10 }

    def on_start(self):
        auto_auth(self)

class EdxUser(HttpLocust):

    task_set = StudentUser
    min_wait=5000
    max_wait=9000
