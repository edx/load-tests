import os
import re
import sys
from config import (
    LOGIN_URL,
    POST_CREDENTIALS_URL,
    ENROLLMENT_URL,
    LOGOUT_URL,
    DASHBOARD_URL,
    INPUT_CHOICE,
    COURSE_URL_PREFIX
)
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'helpers'))

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (
        os.environ['BASIC_AUTH_USER'],
        os.environ['BASIC_AUTH_PASSWORD']
    )


class Certificates(object):
    """
    Base class for page objects.
    """

    def __init__(self, hostname, client):
        """
        Initialize the client.
        :param hostname: The hostname of the test server, sent as the "Referer" HTTP header.
        :param client: The test client used by locust.
        """
        self.hostname = hostname
        self.client = client

        if BASIC_AUTH_CREDENTIALS is not None:
            self.client.auth = BASIC_AUTH_CREDENTIALS

    @property
    def _post_headers(self):
        """
        Headers for a POST request, including the CSRF token.
        """
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname
        }

    def _get(self, url, verify_response_string="", url_group_name=""):
        """
        Make a GET request to the server.
        Skips SSL verification.
        Make the response to fail if verification string is not present on target page
        """
        with self.client.get(url, verify=False, name=url_group_name, catch_response=True) as response:
            if verify_response_string:
                if verify_response_string not in response.content:
                    response.failure("Not on the correct page")
        return response

    def _post(self, *args, **kwargs):
        """
        Make a POST request to the server.
        Skips SSL verification and sends the CSRF cookie.
        """
        kwargs['verify'] = False
        kwargs['headers'] = self._post_headers
        response = self.client.post(*args, **kwargs)
        return response

    def login(self, email, password, remember=False):
        """
        Authenticate the user.
        :param email: The user's email address.
        :param password: The user's password.
        :param remember: Whether "remember me" is checked.
        """
        self.client.get(LOGIN_URL, verify=False)
        url = POST_CREDENTIALS_URL
        params = {
            "email": email,
            "password": password,
            "remember": "true" if remember else "false",
        }
        self._post(url, params)

    def enroll(self, course_key):
        """
        Enroll the user in target course.
        :param course_key:
        """
        url = ENROLLMENT_URL
        course_id = "course-v1:" + course_key
        params = {'course_id': course_id, 'enrollment_action': "enroll"}
        self._post(url, params)

    def attempt_exercise(self, course_key):
        """
        Attempt first exercise to become eligible for certificate
        :param course_key:
        """
        self.client.get(DASHBOARD_URL, verify=False)
        # open the courseware tab
        courseware_url = COURSE_URL_PREFIX + course_key + u"/courseware/"
        courseware_source = self._get(courseware_url)
        # Get the x-block id from source code
        courseware_source_content = courseware_source.content
        block_id = re.search('(?<=type@problem\+block@)\w+', courseware_source_content)
        block_id = block_id.group(0)
        # use the block id to create post request url and question id
        input_id = u"input_" + block_id + u"_2_1"
        answer_url = (
            COURSE_URL_PREFIX +
            course_key +
            u"/xblock/block-v1:" +
            course_key +
            u"+type@problem+block@" +
            block_id +
            u"/handler/xmodule_handler/problem_check"
        )
        params = {input_id: INPUT_CHOICE}
        # Submit the correct answer for mcq
        self._post(answer_url, params)

    def query_certificate(self, user_id, user_name, course_key, group_url_name=""):
        """
        Query the certificate using the url with user id in it
        :param user_id: User ID
        :param user_name: User Name
        :param course_key: Course key
        """
        url = u"/certificates/user/" + str(user_id) + u"/course/course-v1:" + course_key
        certificate_verification_text = "More about " + user_name + "'s accomplishment"
        self._get(url, certificate_verification_text, group_url_name)

    def logout(self):
        """
        Logout the user
        """
        self._get(LOGOUT_URL)
