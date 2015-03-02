""" Load tests for the course content search feature. """

import os
import random

from locust import HttpLocust, TaskSet, task

import constants

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])

# Existing user in the LMS
LMS_USER_EMAIL = os.environ.get('LMS_USER_EMAIL', 'honor@example.com')
LMS_USER_PASSWORD = os.environ.get('LMS_USER_PASSWORD', 'edx')


class LMSPage(object):
    """Base class for page objects. """

    def __init__(self, hostname, client):
        """Initialize the client.

        Arguments:
            hostname (unicode): The hostname of the test server, sent as the "Referer" HTTP header.
            client (Session): The test client used by locust.

        """
        self.hostname = hostname
        self.client = client

        if BASIC_AUTH_CREDENTIALS is not None:
            self.client.auth = BASIC_AUTH_CREDENTIALS

    def get(self, url):
        """HTTP GET request.

        Disables SSL verification, which may not be set up in the test environment.

        Arguments:
            url (unicode): The URL end-point used to make the request.

        Returns:
            Response

        """
        return self.client.get(url, verify=False)

    def post(self, url, params):
        """HTTP POST request.

        Includes CSRF token header and disables SSL verification.

        Arguments:
            url (unicode): The URL end-point used to make the request.
            params (dict): The POST params to send with the request.

        Returns:
            Response

        """
        return self.client.post(
            url,
            params,
            headers=self._post_headers,
            verify=False
        )

    def login(self, email, password, remember=False):
        """Log in using the login page. """
        params = {
            "email": email,
            "password": password,
            "remember": "true" if remember else "false",
        }
        self.post("/login_ajax", params)

    def search(self, search_path, search_string, page_size=20, page_index=0):
        """Search the course using the courseware page. """
        params = {
            "search_string": search_string,
            "page_size": page_size,
            "page_index": page_index,
        }
        self.post(search_path, params)

    @property
    def _post_headers(self):
        """Headers for a POST request, including the CSRF token. """
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname
        }


class UserBehavior(TaskSet):
    """User scripts that exercise the course content search feature. """

    def on_start(self):
        """Initialize the test. """
        self.page = LMSPage(self.locust.host, self.client)
        self._login_success()

    def _login_success(self):
        """Simulate a successful login. """
        self.page.get("/login")
        self.page.login(LMS_USER_EMAIL, LMS_USER_PASSWORD)

    @task
    def course_searching(self):
        """Simulate course content search. """
        course_id = random.choice(constants.COURSES)
        search_phrase = random.choice(constants.SEARCH_PHRASES[course_id])
        search_path = "/search/{}".format(course_id)
        self.page.search(search_path, search_phrase)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
