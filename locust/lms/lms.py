"""
"""

import logging
import os
import re

from lazy import lazy
from locust import task, TaskSet
from opaque_keys.edx.keys import CourseKey

import course_data


BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (
        os.environ['BASIC_AUTH_USER'],
        os.environ['BASIC_AUTH_PASSWORD']
    )


class EdxAppTasks(TaskSet):
    """
    Methods useful to any/all HTTP tests for edx-platform (i.e. LMS or Studio).
    """

    def __init__(self, *args, **kwargs):
        """
        Add basic auth credentials to our client object when specified.
        """
        super(EdxAppTasks, self).__init__(*args, **kwargs)
        if BASIC_AUTH_CREDENTIALS:
            self.client.auth = BASIC_AUTH_CREDENTIALS

        self._user_id = None
        self._username = None
        self._email = None
        self._password = None

    def auto_auth(self):
        """
        Logs in with a new, programmatically-generated user account.
        Requires AUTO_AUTH functionality to be enabled in the target edx instance.
        """
        if "sessionid" in self.client.cookies:
            del self.client.cookies["sessionid"]

        response = self.client.get("/auto_auth", name="auto_auth")
        match = re.search(
            r'Logged in user ([\w]+) \(([\w@\.]+)\) with password ([\w]+) and user_id ([\d]+)',
            response.text
        )
        self._username, self._email, self._password, self._user_id = match.groups()

    @lazy
    def course_id(self):
        """
        The complete id of the course we're configured to test with.
        """
        return os.getenv('COURSE_ID', 'edX/DemoX/Demo_Course')

    @lazy
    def course_key(self):
        """
        The 'org' part of the course_id.
        """
        return CourseKey.from_string(self.course_id)

    @lazy
    def course_org(self):
        """
        The 'org' part of the course_id.
        """
        return self.course_key.org

    @lazy
    def course_num(self):
        """
        The 'num' (aka 'course') part of the course_id.
        """
        return self.course_key.course

    @lazy
    def course_run(self):
        """
        The 'run' part of the course_id.
        """
        return self.course_key.run

    @lazy
    def course_data(self):
        """
        Accessor for the CourseData instance we're configured to test with.
        """
        course_data_name = os.getenv('COURSE_DATA', 'demo_course')
        return getattr(course_data, course_data_name)

    @property
    def post_headers(self):
        """
        Boilerplate headers for HTTP POST.
        """
        return {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host
        }

    @task
    def stop(self):
        """
        Supports usage as nested or top-level task set.
        """
        if self.parent != self.locust:
            self.interrupt()


class LmsTasks(EdxAppTasks):
    """
    Base class for course-specific LMS TaskSets.

    This class supports environment-based configuration to override default values
    for the following:

    * COURSE_ID: pass the course_id against which requests should be made.
    * COURSE_DATA: pass the name of a CourseData object, which should be importable
    from the `course_data` subpackage.  Obviously, the id and the data should
    correlate, or you're likely to see a high error rate in your results.
    """

    def enroll(self):
        """
        Enrolls the test's user in the course under test.
        """
        self.client.post(
            '/change_enrollment',
            data={'course_id': self.course_id, 'enrollment_action': 'enroll'},
            headers=self.post_headers,
            name='enroll',
        )

    def _request(self, method, path, *args, **kwargs):
        """
        Single internal helper for setting up course-specific LMS requests.
        """
        path = '/courses/{course_id}/' + path
        path = path.format(**{n:getattr(self, n) for n in ('course_id', 'course_num', 'course_run', 'course_org')})
        logging.debug(path)
        return getattr(self.client, method)(path, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Perform a GET, contextualizing the path for the course under test.

        String formatting placeholders for 'course_id', 'course_num', 'course_run', 'course_org'
        in the passed path will be evaluated and replaced.
        """
        return self._request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Perform a POST, contextualizing the path for the course under test, and adding any
        mandatory request headers not explicitly passed in the call.

        String formatting placeholders for 'course_id', 'course_num', 'course_run', 'course_org'
        in the passed path will be evaluated and replaced.
        """
        headers = self.post_headers
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        return self._request('post', *args, **kwargs)

    def on_start(self):
        """
        """
        self.auto_auth()
        self.enroll()
