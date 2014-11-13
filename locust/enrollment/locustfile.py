"""
Performance tests for enrollment API.

To start the test server on the host "www.example.com":

    >>> BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password locust --host https://www.example.com

Then visit http://localhost:8089/

You can omit basic auth credentials if the test server is not protected by basic auth.

This test REQUIRES that auto auth is enabled in the test environment.
To enable auto auth, set the feature flag `AUTOMATIC_AUTH_FOR_TESTING` to True.

By default, the test uses the demo course to enroll/unenroll students.
You can override this by setting the environment var `COURSE_ID` to a slash-separated course key.

"""

import os
import json
from locust import HttpLocust, TaskSet, task


# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])


# Course ID
COURSE_ID = os.environ.get('COURSE_ID', 'edX/DemoX/Demo_Course')


class EnrollmentApi(object):
    """Interact with the enrollment API. """
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

    def get_student_enrollments(self):
        """Retrieve enrollment info for the currently logged in user. """
        self.client.get("/enrollment/v0/student", verify=False)

    def enroll(self, course_id):
        """Enroll the user in `course_id`. """
        url = u"{base}/{course_id}".format(
            base="/enrollment/v0/course",
            course_id=course_id
        )
        self.client.post(
            url,
            headers=self._post_headers,
            verify=False
        )

    def unenroll(self, course_id):
        """Unenroll the user from `course_id`. """
        url = u"{base}/{course_id}".format(
            base="/enrollment/v0/course",
            course_id=course_id
        )
        params = json.dumps({"deactivate": True})
        self.client.post(url, params, headers=self._post_headers, verify=False)

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
    """User scripts that exercise the combined login/registration page. """

    def on_start(self):
        """Initialize the test. """
        self.api = EnrollmentApi(self.locust.host, self.client)

    @task
    def enroll_student(self):
        """Enroll a student in a course. """
        self._auto_auth()
        self.api.enroll(COURSE_ID)
        self.api.get_student_enrollments()

    @task
    def unenroll_and_reenroll_student(self):
        """Unenroll a student from a course. """
        self._auto_auth()
        self.api.enroll(COURSE_ID)
        self.api.unenroll(COURSE_ID)
        self.api.enroll(COURSE_ID)
        self.api.get_student_enrollments()

    def _auto_auth(self):
        """Create a new account with random credentials and log in.

        This requires that the test server has the feature flag
        `AUTOMATIC_AUTH_FOR_TESTING` set to True.

        """
        del self.client.cookies["sessionid"]
        self.client.get("/auto_auth", verify=False)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
