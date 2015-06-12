""" Load tests for the course content search feature. """

import os
import sys
import random

from locust import HttpLocust, task

# Work around the fact that Locust runs locustfiles as scripts within packages
# and therefore doesn't allow the use of absolute or explicit relative imports.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'helpers'))
from auto_auth_tasks import AutoAuthTasks
import constants

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])


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


class UserBehavior(AutoAuthTasks):
    """User scripts that exercise the course content search feature. """

    def on_start(self):
        """Initialize the test. """
        self.page = LMSPage(self.locust.host, self.client)
        self.auto_auth()

    @task
    def course_searching(self):
        """Simulate course content search. """
        course_id = random.choice(constants.COURSE_IDS)
        search_phrase = random.choice(constants.SEARCH_PHRASES)
        search_path = "/search/{}".format(course_id)
        self.page.search(search_path, search_phrase)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 30
    max_wait = 50
