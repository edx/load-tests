import os
import random
from locust import HttpLocust, TaskSet, task

COURSES = ['edX/DemoX/Demo_Course', 'LinuxFoundationX/LFS101x/2T2014', 'ANUx/ANU-ASTRO2x/2T2014']

LMS_URL = os.environ.get('LMS_URL')

if not LMS_URL:
    raise Exception('LMS_URL must be set to the URL of a functioning LMS instance!')

LMS_USERNAME = os.environ.get('LMS_USERNAME')
LMS_PASSWORD = os.environ.get('LMS_PASSWORD')

if not (LMS_USERNAME and LMS_PASSWORD):
    raise Exception('LMS_USERNAME and LMS_PASSWORD must both be set!')

BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')
BASIC_AUTH_CREDENTIALS = None

if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
    BASIC_AUTH_CREDENTIALS = (BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)


class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        lms_login = '{}/login'.format(LMS_URL)
        lms_login_ajax = '{}/login_ajax'.format(LMS_URL)

        # Set basic auth credentials, if necessary (e.g. for edX stage environment)
        if BASIC_AUTH_CREDENTIALS:
            self.client.auth = BASIC_AUTH_CREDENTIALS

        # Make a call to the login page to get cookies (esp. CSRF token)
        self.client.get(lms_login)

        # Set the headers and data for the actual login request.
        headers = {
            'referer': lms_login
        }
        data = {
            'email': LMS_USERNAME,
            'password': LMS_PASSWORD,
            'csrfmiddlewaretoken': self.client.cookies['csrftoken']
        }

        # Login!
        r = self.client.post(lms_login_ajax, data=data, headers=headers)
        try:
            success = r.json().get('success', False)
        except Exception as e:
            raise Exception('Login failed: ' + r.text)

        if not success:
            raise Exception('Login failed!')

        # Remove the basic auth credentials
        self.client.auth = None

        # Log into Insights
        self.client.get("/", allow_redirects=True)

    def get_course_path(self, course_id=None, path=None):
        course_id = course_id or random.choice(COURSES)
        path = path or ''

        self.client.get("/courses/{0}/{1}".format(course_id, path))

    @task
    def index(self):
        self.client.get("/")

    @task
    def course_enrollment_activity(self):
        self.get_course_path(path='enrollment/activity/')

    @task
    def course_enrollment_geography(self):
        self.get_course_path(path='enrollment/geography/')

    @task
    def course_engagement_content(self):
        self.get_course_path(path='engagement/content/')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
