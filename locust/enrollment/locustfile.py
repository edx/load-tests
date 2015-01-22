"""
Performance tests for enrollment API.

To start the test server on the host "www.example.com":

    >>> BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password locust --host https://www.example.com

Then visit http://localhost:8089/

You can omit basic auth credentials if the test server is not protected by basic auth.

This test REQUIRES that auto auth is enabled in the test environment.
To enable auto auth, set the feature flag `AUTOMATIC_AUTH_FOR_TESTING` to True.

By default, the test uses the demo course to enroll/unenroll students.
You can override this by setting the environment var `COURSE_ID_LIST` to a comma-separated list
of slash-separated course keys.

"""

import os
import json
import uuid
import random
from locust import HttpLocust, TaskSet, task


# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])


# Course ID
COURSE_ID_LIST = os.environ.get('COURSE_ID_LIST', 'edX/DemoX/Demo_Course').split(",")

EMAIL_USERNAME = "success"
EMAIL_URL = "simulator.amazonses.com"
# Set a password for the users
USER_PASSWORD = "test"
ENROLLMENT_API_BASE_URL = "/api/enrollment/v1"


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
        self.client.get("{0}/enrollment".format(ENROLLMENT_API_BASE_URL), verify=False)

    def enroll(self, course_id):
        """Enroll the user in `course_id`. """
        url = u"{base}/enrollment".format(
            base=ENROLLMENT_API_BASE_URL
        )
        params = {'course_details': {'course_id': course_id}}
        self.client.post(
            url,
            json.dumps(params),
            headers=self._post_headers,
            verify=False
        )

    def get_user_enrollment_status(self, user_name, course_id):
        """Check the user enrollment status in a given course. """
        url = u"{base}/enrollment/{user},{course_key}".format(
            base=ENROLLMENT_API_BASE_URL,
            user=user_name,
            course_key=course_id
        )
        name = u"{base}/enrollment/{{user}},{{course_key}}".format(base=ENROLLMENT_API_BASE_URL)
        self.client.get(url, verify=False, name=name)

    def get_enrollment_detail_for_course(self, course_id):
        """Get enrollment details for a course. """
        url = u"{base}/course/{course_key}".format(
            base=ENROLLMENT_API_BASE_URL,
            course_key=course_id
        )
        name = u"{base}/course/{{course_key}}".format(base=ENROLLMENT_API_BASE_URL)
        self.client.get(url, verify=False, name=name)

    @property
    def _post_headers(self):
        """Headers for a POST request, including the CSRF token. """
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname
        }


class AutoAuthTaskSet(TaskSet):
    """Use the auto-auth end-point to create test users. """

    def auto_auth(self):
        """Create a new account with given credentials and log in.

        This requires that the test server has the feature flag
        `AUTOMATIC_AUTH_FOR_TESTING` set to True.

        """
        del self.client.cookies["sessionid"]
        self.username = "{0}{1}".format(EMAIL_USERNAME, uuid.uuid4().hex[:20])
        self.full_email = "{0}@{1}".format(self.username, EMAIL_URL)
        params = {
            'password': USER_PASSWORD,
            'email': self.full_email,
            'username': self.username,
        }
        self.client.get("/auto_auth", params=params, verify=False, name="/auto_auth")
        return self.username


class UserBehavior(TaskSet):
    """User scripts that exercise the enrollment API. """

    @task(300)
    class AuthenticatedAndEnrolledTasks(AutoAuthTaskSet):
        """User scripts in which the user is already authenticated and enrolled. """

        def on_start(self):
            """Ensure the user is logged in and enrolled. """
            self.api = EnrollmentApi(self.locust.host, self.client)
            self.auto_auth()

            # Ensure that the user is enrolled in all the courses
            for course_id in COURSE_ID_LIST:
                self.api.enroll(course_id)

        @task
        def user_enrollment_status(self):
            """Check a user's enrollment status in a course. """
            course_id = random.choice(COURSE_ID_LIST)
            self.api.get_user_enrollment_status(self.username, course_id)

        @task
        def list_enrollments(self):
            """Get all enrollments for a user. """
            self.api.get_student_enrollments()

    @task(300)
    class AuthenticatedButNotEnrolledTasks(AutoAuthTaskSet):
        """User scripts in which the user is authenticated but not enrolled. """

        def on_start(self):
            """Ensure the user is logged in """
            self.api = EnrollmentApi(self.locust.host, self.client)
            self.auto_auth()

        @task
        def user_enrollment_status(self):
            """Check a user's enrollment status in a course. """
            course_id = random.choice(COURSE_ID_LIST)
            self.api.get_user_enrollment_status(self.username, course_id)

        @task
        def list_enrollments(self):
            """Get all enrollments for a user. """
            self.api.get_student_enrollments()

    @task(300)
    class NotAuthenticatedTasks(TaskSet):
        """User scripts in which the user is not authenticated. """

        def on_start(self):
            self.api = EnrollmentApi(self.locust.host, self.client)

        @task
        def enrollment_detail_for_course(self):
            """Retrieve enrollment details for a course. """
            course_id = random.choice(COURSE_ID_LIST)
            self.api.get_enrollment_detail_for_course(course_id)

    @task(1)
    class EnrollNewUserTasks(AutoAuthTaskSet):
        """User scripts to enroll a user into a course for the first time. """

        def on_start(self):
            self.api = EnrollmentApi(self.locust.host, self.client)
            self._reset()

        @task
        def enroll(self):
            """First-time enrollment in a course. """
            # Since we can only enroll in a course once,
            # restart as a new user once we run out of courses.
            try:
                course_id = next(self.course_ids)
            except StopIteration:
                self._reset()
            else:
                self.api.enroll(course_id)

        def _reset(self):
            """Log in as a new user (with no enrollments). """
            self.auto_auth()
            self.course_ids = iter(COURSE_ID_LIST)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
