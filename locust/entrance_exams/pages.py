import os
import re
import sys
import logging
from config import COURSE_URL_PREFIX

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'helpers'))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (
        os.environ['BASIC_AUTH_USER'],
        os.environ['BASIC_AUTH_PASSWORD']
    )


class BasePage(object):
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

    def _post(self, *args, **kwargs):
        """Perform a POST."""
        kwargs['headers'] = self._post_headers
        # Bypass SSL certificate verification
        kwargs['verify'] = False
        return self._request('post', *args, **kwargs)

    @property
    def _post_headers(self):
        """Boilerplate headers for HTTP POST requests."""
        return {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }

    def _request(self, method, path, *args, **kwargs):
        """Single internal helper for setting up requests."""
        logger.debug(path)
        return getattr(self.client, method)(path, *args, **kwargs)

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


class ExamPage(BasePage):
    """
    Base class for page objects.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(ExamPage, self).__init__(*args, **kwargs)

    def fetch_exam_url(self, course_id, lesson_name, url_name):
        """
        fetch urls for exam pages from course ware source code
        :param course_id, lesson_name, url_name
        :return: url plus name for specific exam
        """
        exam_info = []
        # open the courseware tab
        courseware_url = COURSE_URL_PREFIX + course_id + u"/courseware"
        courseware_source = self._get(courseware_url, url_group_name=url_name)
        # Get the exam url from source page
        courseware_source_content = courseware_source.content
        lesson_id_search = re.search(r'[^<]+(?=<p>(' + lesson_name + '))', courseware_source_content)
        lesson_id = lesson_id_search.group(0)
        exam_url_search = re.search(r'(?<=")(.*)(?=")', lesson_id)
        exam_url = exam_url_search.group(0)
        return exam_url

    def load_courseware(self, course_id, url_name):
        """
        Load the courseware
        :param course_id, url_name:
        :return:
        """
        courseware_url = COURSE_URL_PREFIX + course_id + '/courseware'
        self._get(courseware_url, url_group_name=url_name)

    def load_exam(self, exam_url, url_name):
        """
        Load exam page using exam url
        :param exam_info, url_name:
        """
        # open the exam page
        exam_url = exam_url
        self._get(exam_url, url_group_name=url_name)

    def exam_attempt(self, course_id, exam_url, choice, choice_type, url_name):
        """
        Attempt first exercise to become eligible for certificate
        :param course_id, exam_info, choice, choice_type, url_name:
        """
        # open the exam page
        exam_url = exam_url
        exam_source = self._get(exam_url, url_group_name=url_name)
        # Get the x-block id from source code
        exam_source_content = exam_source.content
        block_id = re.search('(?<=type@problem\+block@)\w+', exam_source_content)
        block_id = block_id.group(0)
        # use the block id to create post request url and question id
        input_id = u"input_" + block_id + u"_2_1"
        course_key = course_id.replace('course-v1:', '')
        answer_url = (
            COURSE_URL_PREFIX +
            course_id +
            u"/xblock/block-v1:" +
            course_key +
            u"+type@problem+block@" +
            block_id +
            u"/handler/xmodule_handler/problem_check"
        )
        params = {input_id: choice}
        # Submit the correct answer for mcq
        post_response = self._post(answer_url, data=params)
        attempt_status = post_response.json()['success']
        if attempt_status != choice_type:
            raise ValueError('Attempt status is not as expected')


class InstructorPage(BasePage):
    """
    Base class for page objects.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(InstructorPage, self).__init__(*args, **kwargs)

    def go_to_instructor_dashboard(self, course_id):
        """
        Go to the instructor dashboard of target course
        :param course_id, student_username:
        """
        course_info_url = COURSE_URL_PREFIX + course_id + u"/info"
        self._get(course_info_url)
        # Go to instructor tab
        staff_view_url = COURSE_URL_PREFIX + course_id + u"/instructor"
        self._get(staff_view_url)
        # perform different actions
        action_api_url = COURSE_URL_PREFIX + course_id + u"/instructor/api"
        return action_api_url

    def reset_attempt(self, student_username, action_api_url):
        """
        Perform Entrance Exam related task from Instructor Dashboard
        :param student_username, action_api_url:
        """
        reset_attempt_url = (
            action_api_url +
            u"/reset_student_attempts_for_entrance_exam?unique_student_identifier=" +
            student_username +
            "&delete_module=false"
        )
        self._get(reset_attempt_url, url_group_name='[Reset Student Attempt]')

    def rescore_exam(self, student_username, action_api_url):
        """
        Perform Entrance Exam related task from Instructor Dashboard
        :param student_username, action_api_url:
        """
        rescore_exam_url = (
            action_api_url +
            u"/rescore_entrance_exam?unique_student_identifier=" +
            student_username
        )
        self._get(rescore_exam_url, url_group_name='[Rescore Student Exams]')

    def delete_attempt(self, student_username, action_api_url):
        """
        Perform Entrance Exam related task from Instructor Dashboard
        :param student_username, action_api_url:
        """
        delete_attempt_url = (
            action_api_url +
            u"/reset_student_attempts_for_entrance_exam?unique_student_identifier=" +
            student_username +
            "&delete_module=true"
        )
        self._get(delete_attempt_url, url_group_name='[Delete Student Attempt]')

    def skip_exam(self, student_username, action_api_url):
        """
        Perform Entrance Exam related task from Instructor Dashboard
        :param student_username, action_api_url:
        """
        skip_exam_url = action_api_url + u"/mark_student_can_skip_entrance_exam"
        params = {'unique_student_identifier': student_username}
        self._post(skip_exam_url, data=params)
