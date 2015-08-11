"""
Load tests for the courseware student module.
"""

import os
import random
import sys
import time

from locust import HttpLocust, TaskSet, task, events

# Work around the fact that Locust runs locustfiles as scripts within packages
# and therefore doesn't allow the use of absolute or explicit relative imports.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'helpers'))
import constants

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'],
                              os.environ['BASIC_AUTH_PASSWORD'])

# Existing user in the LMS
LMS_USER_EMAIL = os.environ.get('LMS_USER_EMAIL')
LMS_USER_PASSWORD = os.environ.get('LMS_USER_PASSWORD')

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
        response = self.post("/login_ajax", params)
        print response.text

    def post_response(self, path, payload):
        self.post(path, payload)

    @property
    def _post_headers(self):
        """Headers for a POST request, including the CSRF token. """
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname
        }


class QuestionResponse(TaskSet):
    "Respond to a question in the LMS."

    def on_start(self):
        "Setup method; log in to the LMS."

        self.page = LMSPage(self.locust.host, self.client)
        if BASIC_AUTH_CREDENTIALS:
            self.client.auth = BASIC_AUTH_CREDENTIALS
        self.client.get("/")
        self.page.login(LMS_USER_EMAIL, LMS_USER_PASSWORD)

    @task
    def respond_to_question(self):
        "Respond to question."
        uri = random.choice(constants.QUESTION_POST_DATA.keys())
        payload = constants.QUESTION_POST_DATA[uri]
        self.page.post_response(uri, payload)


class WebsiteUser(HttpLocust):
    "Locust user class."

    task_set = QuestionResponse
    min_wait = 10
    max_wait = 50
