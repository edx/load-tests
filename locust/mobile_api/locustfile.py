"""
Load tests for the mobile api.

Usage:

BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=pass locust --host="http://localhost:8000"
"""

import os
import uuid
import json
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

VERBOSE = False
if 'VERBOSE' in os.environ:
    VERBOSE = os.environ['VERBOSE']


class AutoAuthException(Exception):
    """The API returned an HTTP status 403 """
    pass


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
    @property
    def _post_headers(self):
        """Headers for a POST request, including the CSRF token. """
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname
        }

    def get_video_summary_list(self, course_id):
        """Call VideoSummaryList with given course_id"""
        url = "{}/video_outlines/courses/{}".format(
            constants.MOBILE_API_BASE_URL,
            course_id
        )
        name = url

        if not VERBOSE:
            name = "GET video_outlines.VideoSummaryList"

        self.client.get(url, name=name)

    def get_video_transcript(self, course_id, block_id, lang):
        """Call VideoTranscripts for given course_id and missing video"""
        url = "{}/video_outlines/transcripts/{}/{}/{}".format(
            constants.MOBILE_API_BASE_URL,
            course_id,
            block_id,
            lang
        )
        name = url

        if not VERBOSE:
            name = "GET video_outlines.VideoTranscripts"

        self.client.get(url, name=name, verify=False)

    def get_user_enrollment_status(self, username, course_set_id):
        """Call UserEnrollmentList for particular user"""
        url = "{}/users/{}/course_enrollments/".format(
            constants.MOBILE_API_BASE_URL,
            username
        )
        name = "{}/users/[{}]/course_enrollments/".format(
            constants.MOBILE_API_BASE_URL, course_set_id)

        if not VERBOSE:
            name = "GET users.UserEnrollmentStatus"

        self.client.get(url, verify=False, name=name)

    def get_course_status_info(self, course_id, username):
        """Call UserCourseStatus with given course_id"""
        url = "{}/users/{}/course_status_info/{}".format(
            constants.MOBILE_API_BASE_URL,
            username,
            course_id
        )
        name = "/api/mobile/v0.5/users/username/course_status_info/{}".format(
            course_id)

        if not VERBOSE:
            name = "GET users.CourseStatus"
        self.client.get(
            url,
            verify=False,
            name=name
            )

    def patch_course_status_info(self, username, course_id, block_id):
        """Patch UserCourseStatus with given block_id"""
        data = {"last_visited_module_id": block_id}
        data = json.dumps(data)
        url = "/api/mobile/v0.5/users/{}/course_status_info/{}".format(
            username, course_id)
        name = "/api/mobile/v0.5/users/[username]/course_status_info/{}".format(
            course_id)

        if not VERBOSE:
            name = "PATCH users.CourseStatus"
        self.client.patch(
            url=url,
            data=data,
            headers=self._post_headers,
            verify=False,
            name=name
        )

    def get_user_detail(self, username):
        """Call UserDetail for given username"""
        url = "{}/users/{}".format(
            constants.MOBILE_API_BASE_URL,
            username
        )
        name = "{}/users/[username]".format(constants.MOBILE_API_BASE_URL)

        if not VERBOSE:
            name = "GET users.UserDetail"
        self.client.get(url, name=name, verify=False)
        
    def get_course_updates_list(self, course_id):
        """Call CourseUpdatesList for given course_id"""
        url = "{}/course_info/{}/updates".format(
            constants.MOBILE_API_BASE_URL,
            course_id
        )
        name = url

        if not VERBOSE:
            name = "GET course_info.CourseUpdatesList"

        self.client.get(url, name=name, verify=False)

    def get_course_handouts_list(self, course_id):
        """Call CourseHandoutsList for given course_id"""
        url = "{}/course_info/{}/handouts".format(
            constants.MOBILE_API_BASE_URL,
            course_id
        )
        name = url

        if not VERBOSE:
            name = "GET course_info.CourseHandoutsList"
        self.client.get(url, name=name, verify=False)



class AutoAuthTaskSet(TaskSet):
    """Use the auto-auth end-point to create test users. """

    def auto_auth(self, username="success", staff="false"):
        """Create a new account with given credentials and log in.

        This requires that the test server has the feature flag
        `AUTOMATIC_AUTH_FOR_TESTING` set to True.
        """

        del self.client.cookies["sessionid"]
        self.username = "{0}{1}".format(username, uuid.uuid4().hex[:20])  # pylint: disable=attribute-defined-outside-init
        self.full_email = "{0}@{1}".format(self.username, constants.EMAIL_URL) # pylint: disable=attribute-defined-outside-init
        params = {
            'password': constants.USER_PASSWORD,
            'email': self.full_email,
            'username': self.username,
            'staff': staff
        }
        response = self.client.get(
            "/auto_auth",
            params=params,
            name="/auto_auth",
        )
        if response.status_code == 200:
            if not response.text.startswith("Logged"):
                print "User creation via auto_auth has failed"
                print response.text[1:50]
                raise AutoAuthException
        else:
            print "User creation via auto_auth has failed"
            print response.url
            print response.status_code
            raise AutoAuthException


class UserBehavior(TaskSet):
    """User scripts that exercises the mobile API"""

    @task(8)
    class VideoSummaryList(AutoAuthTaskSet):
        """
        /api/mobile/v0.5/video_outlines/courses/edx/1/2

        Requires a staff login for access to all courses being tested. Calls the
        url with a random course which is selected in get_course_path.
        """
        min_wait = 10000
        max_wait = 11000

        def on_start(self):
            """Ensure the user is created and logged in"""
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(
                username="vsl",
                staff="true")

        #Normal test
        @task
        def video_summary_list(self):
            """Selects a random course and calls endpoint"""
            course_id = random.choice(constants.ALL_COURSES)
            self.api.get_video_summary_list(course_id)

        # #Split vs Mongo
        # @task
        # def video_summary_list(self):
        #     """Selects a random course and calls endpoint"""
        #     course_id = random.choice(constants.COURSE_ID_LIST_SMALL_C)
        #     self.api.get_video_summary_list(course_id)

    @task(9)
    class VideoTranscript(AutoAuthTaskSet):
        """
        /api/mobile/v0.5/video_outlines/transcripts/edx/1/2/block_id/language

        Requires a staff login for access to all courses being tested. Calls the
        url with a random course which is selected in get_course_path.
        """

        min_wait = 9000
        max_wait = 9000

        def on_start(self):
            """Ensure the user is created and logged in"""
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(
                username="vt",
                staff="true"
            )

        @task
        def video_summary_list(self):
            """
            Selects random video and middle block_id

            The default language is english. The middle video is the location
            of the block_id of the total videos/2.
            """
            course_id = random.choice(constants.ALL_COURSES)
            block_id = constants.MIDDLE_VIDEO_LIST[course_id]
            try:
                #Old mongo
                transcript_id = block_id.split("/video/")[1]
            except IndexError:
                #Split courses
                transcript_id = block_id.split("@video+block@")[1]
            lang = "en"
            self.api.get_video_transcript(course_id, transcript_id, lang)

    @task(5)
    class UserCourseEnrollmentsList(AutoAuthTaskSet):
        """
        /api/mobile/v0.5/users/MRBENJIDOG/course_enrollments/

        Requires a login for the user. Default password can be set.
        Mobile_available needs to be set on a course for it to show up on the
        course_enrollments endpoint. Regardless of mobile available being set
        to true, the endpoint still needs to iterate over the available
        endpoints which is the common case.
        """
        min_wait = 17000
        max_wait = 18000

        #normal
        def on_start(self):
            """Ensure the user is created, logged in and enrolled. """
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init

            #cycles through courses from smallest to largest
            self.course_set_id = constants.COURSE_ID_LIST.pop(0)  # pylint: disable=attribute-defined-outside-init
            constants.COURSE_ID_LIST.append(self.course_set_id)

            self.auto_auth(username=self.course_set_id)
            course_id_list = constants.COURSE_ID_DICT[self.course_set_id]

            for course_id in course_id_list:
                self.api.enroll(course_id)

        # #Large mongo/Large split
        # def on_start(self):
        #     """Ensure the user is craeted, logged in and enrolled. """
        #     self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
        #
        #     self.course_set_id = constants.COURSE_ID_LIST_SMALL_C[0]  # pylint: disable=attribute-defined-outside-init
        #
        #     self.auto_auth(username="mongo", staff="true")
        #     self.api.enroll(self.course_set_id)
        #
        @task
        def user_enrollment_status(self):
            """Gets a particular user's enrollments"""
            self.api.get_user_enrollment_status(
                username=self.username,
                course_set_id=self.course_set_id
            )

    @task(8)
    class UserCourseStatus(AutoAuthTaskSet):
        """
        api/mobile/v0.5/users/staff/course_status_info/edx/1/2

        Requires a staff login for access to all courses being tested. Calls the
        url with a random course which is selected in get_course_path.
        """
        min_wait = 10000
        max_wait = 11000

        #normal
        def on_start(self):
            """Ensure the user is created, logged in and status is set."""
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(
                username="ucs",
                staff="true"
            )

            #cycles through courses from smallest to largest
            self.course_id = constants.ALL_COURSES_STACK.pop(0)  # pylint: disable=attribute-defined-outside-init
            constants.ALL_COURSES_STACK.append(self.course_id)

            self.middle_block_id = constants.MIDDLE_VIDEO_LIST[self.course_id]  # pylint: disable=attribute-defined-outside-init
            self.api.patch_course_status_info(
                username=self.username,
                course_id=self.course_id,
                block_id=self.middle_block_id
            )

        # #old mongo vs split
        # def on_start(self):
        #     """Ensure the user is created, logged in and status is set."""
        #     self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
        #     self.auto_auth(
        #         username="ucs",
        #         staff="true"
        #     )
        #
        #     self.course_id = constants.COURSE_ID_LIST_SMALL_B[0]  # pylint: disable=attribute-defined-outside-init
        #
        #     self.middle_block_id = constants.MIDDLE_VIDEO_LIST[self.course_id]  # pylint: disable=attribute-defined-outside-init
        #     self.api.patch_course_status_info(
        #         username=self.username,
        #         course_id=self.course_id,
        #         block_id=self.middle_block_id
        #     )
        @task
        def course_status_info(self):
            """Selects a random course and calls endpoint"""
            # course_id = random.choice(constants.ALL_COURSES)
            self.api.get_course_status_info(
                course_id=self.course_id,
                username=self.username
            )

    @task(1)
    class CourseUpdatesList(AutoAuthTaskSet):
        """
        {hostname}api/mobile/v0.5/course_info/{course_id}/updates

        Requires staff access or enrollment.
        """

        min_wait = 77000
        max_wait = 77000

        def on_start(self):
            """Ensure the user is created and logged in"""
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(username="cul", staff="true")

        @task
        def course_updates_list(self):
            """Calls the endpoint"""
            course_id = random.choice(constants.ALL_COURSES)
            self.api.get_course_updates_list(course_id)

    @task(1)
    class CourseHandoutsList(AutoAuthTaskSet):
        """
        {hostname}api/mobile/v0.5/course_info/{course_id}/updates

        Requires staff access or enrollment.
        """

        min_wait = 83000
        max_wait = 83000

        def on_start(self):
            """Ensure the user is created and logged in"""
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(username="chl", staff="true")

        @task
        def course_handouts_list(self):
            """Calls the endpoint"""
            course_id = random.choice(constants.ALL_COURSES)
            self.api.get_course_handouts_list(course_id)

    @task(2)
    class UserDetail(AutoAuthTaskSet):
        """GET /api/mobile/v0.5/users/{username}"""

        min_wait = 38000
        max_wait = 39000

        def on_start(self):
            """Ensure the user is created and logged in"""
            self.api = MobileApi(self.locust.host, self.client) # pylint: disable=attribute-defined-outside-init
            self.auto_auth(username="ul",)

        @task
        def user_detail(self):
            """Calls the endpoint"""
            self.api.get_user_detail(username=self.username)


class WebsiteUser(HttpLocust): # pylint: disable=missing-docstring, too-few-public-methods
    task_set = UserBehavior

