import os
import re
import sys
from config import (
    COURSE_URL_PREFIX,
    START_EXAM_URL
)
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'helpers'))

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
        self.default_headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname
        }

    @property
    def _post_headers(self):
        """
        Headers for a POST request, including the CSRF token.
        """
        return self.default_headers

    @_post_headers.setter
    def _post_headers(self, new_headers):
        """
        Headers for a POST request, including the CSRF token.
        """
        self.default_headers = new_headers

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


class ExamPages(BasePage):
    """
    Base class for page objects.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(ExamPages, self).__init__(*args, **kwargs)

    def fetch_exam_url(self, course_id, lesson_name):
        """
        fetch urls for exam pages from courseware source code
        :param course_id, lesson_name
        :return: url plus name for specific exam
        """
        exam_info = []
        info_url = COURSE_URL_PREFIX + course_id + u"/info"
        # open the course info page
        self._get(info_url)
        # open the courseware tab
        courseware_url = COURSE_URL_PREFIX + course_id + u"/courseware/"
        courseware_source = self._get(courseware_url)
        # Get the exam url from source page
        courseware_source_content = courseware_source.content
        lesson_id_search = re.search(r'[^<]+(?=<p>(' + lesson_name + '))', courseware_source_content)
        lesson_id = lesson_id_search.group(0)
        exam_url_search = re.search(r'(?<=")(.*)(?=")', lesson_id)
        exam_info.append(exam_url_search.group(0))
        exam_info.append(lesson_name)
        return exam_info

    def load_start_exam_screen(self, exam_info):
        """
        Load the exam using url and exam name
        :param exam_info:
        :return: exam id
        """
        response = self._get(exam_info[0], url_group_name="lesson_url[" + exam_info[1] + " start_page]")
        search_exam_id = re.search('(?<=data-exam-id=")\d+', response.content)
        return search_exam_id.group(0)

    def start_exam(self, exam_id, exam_info):
        """
        start the exam
        :return:
        """
        csrftoken = self.client.cookies.get('csrftoken', '')
        sessionid = self.client.cookies.get('sessionid', '')
        self._post_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.hostname + exam_info[0],
            'Cookie': 'csrftoken=' + csrftoken + '; sessionid=' + sessionid
        }
        params = {"exam_id": exam_id, "start_clock": "true"}
        self._post(START_EXAM_URL, data=params)

    def load_exam(self, exam_info):
        """
        Load the exam using url and exam name
        :param exam_info:
        :return:
        """
        self._get(exam_info[0], url_group_name="lesson_url[" + exam_info[1] + "]")
