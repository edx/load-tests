"""
Load tests for the mobile api.

Usage:

BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=pass locust --host="http://localhost:8000"
"""

import os
import json
import uuid
import random
import constants
from locust import HttpLocust, TaskSet, task


# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (
        os.environ['BASIC_AUTH_USER'],
        os.environ['BASIC_AUTH_PASSWORD']
    )


class MobileApi(object):
    """Interact with the Mobile API. """
    def __init__(self, hostname, client):
        """
        Initialize the client.

        Arguments:
            hostname (unicode): The hostname of the test server, sent as the
                "Referer" HTTP header.
            client (Session): The test client used by locust.

        """
        self.hostname = hostname
        self.client = client

        if BASIC_AUTH_CREDENTIALS is not None:
            self.client.auth = BASIC_AUTH_CREDENTIALS

    def enroll(self, course_id):
        """Enroll the user in `course_id`. """
        url = u"{}/enrollment".format(constants.ENROLLMENT_API_BASE_URL)
        params = {'course_details': {'course_id': course_id}}
        response = self.client.post(
            url,
            json.dumps(params),
            headers=self._post_headers,
            verify=False
        )
        if response.status_code == 400:
            print course_id, response

    def get_video_summary_list(self, course_id):
        """Call VideoSummaryList with given course_id"""
        url = "{}/video_outlines/courses/{}".format(
            constants.MOBILE_API_BASE_URL,
            course_id
        )
        self.client.get(url, verify=False)

    def get_course_status_info(self, course_id, username):
        """Call UserCourseStatus with given course_id"""
        url = "{}/users/{}/course_status_info/{}".format(
            constants.MOBILE_API_BASE_URL,
            username,
            course_id
        )
        self.client.get(url, verify=False)

    def get_user_enrollment_status(self, username):
        """Call UserEnrollmentList for particular user"""
        url = "{}/users/{}/course_enrollments/".format(
            constants.MOBILE_API_BASE_URL,
            username
        )
        self.client.get(url, verify=False)


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

    def auto_auth(self, email_username="success", staff_access="false"):
        """Create a new account with given credentials and log in.

        This requires that the test server has the feature flag
        `AUTOMATIC_AUTH_FOR_TESTING` set to True.

        """

        del self.client.cookies["sessionid"]
        self.username = "{0}{1}".format(email_username, uuid.uuid4().hex[:20])  # pylint: disable=attribute-defined-outside-init
        self.full_email = "{0}@{1}".format(self.username, constants.EMAIL_URL) # pylint: disable=attribute-defined-outside-init
        params = {
            'password': constants.USER_PASSWORD,
            'email': self.full_email,
            'username': self.username,
            'staff': staff_access
        }
        self.client.get(
            "/auto_auth",
            params=params,
            verify=False,
            name="/auto_auth",
        )
        return self.username


class UserBehavior(TaskSet):
    """User scripts that exercises the mobile API"""

    @task(6)
    class VideoSummaryList(AutoAuthTaskSet):
        """
        /api/mobile/v0.5/video_outlines/courses/edx/1/2

        Requires a staff login for access to all courses being tested. Calls the
        url with a random course which is selected in get_course_path.
        """

        def on_start(self):
            """Ensure the user is logged in and enrolled. """
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(
                email_username="videolist",
                staff_access="true")

        @task
        def video_summary_list(self):
            """Selects a random course and GETs the endpoint"""
            course_id = random.choice(constants.COURSE_ID_LIST["XLARGE"])
            self.api.get_video_summary_list(course_id)


    @task(13)
    class UserCourseStatus(AutoAuthTaskSet):
        """
        api/mobile/v0.5/users/staff/course_status_info/edx/1/2

        Requires a staff login for access to all courses being tested. Calls the
        url with a random course which is selected in get_course_path.
        """
        def on_start(self):
            """Ensure the user is logged in and enrolled."""
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(
                email_username="videolist",
                staff_access="true")

        @task
        def course_status_info(self):
            """Selects a random course and GETs the endpoint"""
            course_id = random.choice(constants.COURSE_ID_LIST["XLARGE"])
            self.api.get_course_status_info(course_id, username=self.username)

    @task(7)
    class UserCourseEnrollmentsList(AutoAuthTaskSet):
        """
        /api/mobile/v0.5/users/MRBENJIDOG/course_enrollments/

        Requires a login for the user. Default password can be set.
        Mobile_available needs to be set on a course for it to show up on the
        course_enrollments endpoint. Regardless of mobile available being set
        to true, the endpoint still needs to iterate over the available
        endpoints which is the common case.
        """

        def on_start(self):
            """Ensure the user is logged in and enrolled. """
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            course_id_username = random.choice(constants.COURSE_ID_LIST.keys())
            self.auto_auth(email_username=course_id_username)
            course_id_list = constants.COURSE_ID_LIST[course_id_username]

            for course_id in course_id_list:
                self.api.enroll(course_id)

        @task
        def user_enrollment_status(self):
            """Gets a particular user's enrollments"""
            self.api.get_user_enrollment_status(username=self.username)


class WebsiteUser(HttpLocust): # pylint: disable=missing-docstring, too-few-public-methods
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
