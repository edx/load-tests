"""
Load tests for the course_overviews course metadata caching framework.

Environment variables:

    ENDPOINT_TO_TEST
        Values: user_course_enrollments_list, student_dashboard
        Specifies the API endpoint that the locusts will swarm after enrolling.
        Required.

    BASIC_AUTH
        Format: username,password
        Specifies the basic auth credentials for the target server.
        Optional; defaults to no basic auth.

    LOGGING_LEVEL
        Values: none, error, all
        How much logging output to display.
        Optional; defaults to error.

    DEVELOPER_MODE
        Values: True, False
        Whether the test is in development mode. Locusts will be enrolled in
            a different set of courses if this values is set to True in order
            to avoid warming up the CourseOverview cache during development.
        Optional; defaults to False.

How the test works:
    - Load up a list of course keys from all-courses.json.
    - Create a pool of Draft course keys and a pool of Split course keys based
      the value of COURSE_POOL_SIZE.
    - For every locust spawned:
        - Create and log in a user with a globally unique (even between runs of
          the load test) username using the /auto_auth service.
        - Based on {SPLIT,DRAFT}_COURSES_PER_USER, select a random set of Draft
          and Split course keys from the course key pool.
        - Enroll the user in the selected courses.
        - For every USER_WAIT_MS_PER_QUERY ms until the end of the test:
            - Query ENDPOINT_TO_TEST.
"""

import inspect
import itertools
import json
import locust
import os
import random
import re


# Logging levels
LOG_NONE = 0
LOG_ERROR = 1
LOG_ALL = 2

# Environment variable options; initialized in init_environment_variables
ENDPOINT_TO_TEST = None
BASIC_AUTH = None
LOGGING_LEVEL = None
DEVELOPER_MODE = None

# Load parameters
USER_WAIT_MS_PER_QUERY = 1000
DRAFT_COURSES_PER_USER = 5
SPLIT_COURSES_PER_USER = 5
COURSE_POOL_SIZE = 75
DEV_COURSE_POOL_SIZE = 10

# Because we want this test to be repeatable, all the random number
# generators used are seeded with deterministic values based on the
# value of RANDOM_GEN_SEED. In order to run the test with different
# random courses, change the value of RANDOM_GEN_SEED.
# The initial value of 0 here is arbitrary.
RANDOM_GEN_SEED = 0

# Certain courses have been returning error statuses when the locusts try to
# enroll in them.
# Instead of trying to figure out what's wrong, let's just filter them out.
BAD_DRAFT_COURSE_KEYS = [
    "Ethicon/MARS2014-1x/2014_1"
]
BAD_SPLIT_COURSE_KEYS = [
    "course-v1:HarvardX+SW25x.1+2015"
]

# URLs
AUTO_AUTH_API_BASE_URL = u"/auto_auth"
ENROLLMENT_API_BASE_URL = u"/api/enrollment/v1"
MOBILE_API_BASE_URL = u"/api/mobile/v0.5"
DASHBOARD_BASE_URL = u"/dashboard"


def init_environment_variables():
    """
    Initializes configuration options from environment variables.

    Should be called exactly once near the beginning of the test.
    """
    global ENDPOINT_TO_TEST, BASIC_AUTH, LOGGING_LEVEL, DEVELOPER_MODE  # pylint: disable=global-statement

    valid_test_endpoints = ['user_course_enrollments_list', 'student_dashboard']
    ENDPOINT_TO_TEST = os.environ.get('ENDPOINT_TO_TEST', None)
    if ENDPOINT_TO_TEST not in valid_test_endpoints:
        raise Exception(
            "Must specify ENDPOINT_TO_TEST as one of: " +
            ", ".join(valid_test_endpoints)
        )

    basic_auth_string = os.environ.get('BASIC_AUTH', None)
    BASIC_AUTH = tuple(basic_auth_string.split(',')) if basic_auth_string else None

    DEVELOPER_MODE = os.environ.get('DEVELOPER_MODE', 'false').lower() == 'true'

    log_levels = {
        'none': LOG_NONE,
        'error': LOG_ERROR,
        'all': LOG_ALL
    }
    logging_level_string = os.environ.get('LOGGING_LEVEL', 'error').lower()
    if logging_level_string in log_levels:
        LOGGING_LEVEL = log_levels[logging_level_string]
    else:
        raise Exception("LOGGING_LEVEL must be one of: " + ", ".join(log_levels.keys()))


init_environment_variables()


def _get_current_function_name():
    """
    Returns the name (str) of the caller by inspecting the stack.
    """
    return inspect.stack()[1][3]


def log(format_string, *format_args):
    """
    Prints logging output.

    Arguments:
        format_string (basestring): Formatting string using {} syntax.
        *format_args (list[Any]): Formatting arguments.
    """
    if LOGGING_LEVEL >= LOG_ALL:
        print format_string.format(*format_args)


def log_error(format_string, *format_args):
    """
    Prints error output.

    Arguments:
        format_string (basestring): Formatting string using {} syntax.
        *format_args (list[Any]): Formatting arguments.
    """
    if LOGGING_LEVEL >= LOG_ERROR:
        os.sys.stderr.write(format_string.format(*format_args) + "\n")


class TestApi(object):
    """
    Class for interacting with the different APIs that we'll be testing.
    """

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
        if BASIC_AUTH:
            self.client.auth = BASIC_AUTH

    def create_and_log_in_user(self, is_staff):
        """
        Create a new user with a random username and log them in.

        Requires that the test server has the feature flag
        AUTOMATIC_AUTH_FOR_TESTING enabled.

        Arguments:
            is_staff (bool): Whether the user is to be staff.

        Returns:
            unicode: Username of the created user.

        Raises:
            IOError if the user creation fails.
        """
        response = self.client.get(
            url=AUTO_AUTH_API_BASE_URL,
            params={'staff': unicode(is_staff).lower()},
            name=_get_current_function_name()
        )
        if response.status_code == 200:
            match = re.search(r'(Logged in|Created) user (?P<username>[^$]+).*', response.text)
            if match:
                username = match.group('username')
                log("Successfully created and logged in user {}", username)
                return unicode(username)

        raise IOError(
            "Failed to authorize user. Response (status {}): {}".format(
                response.status_code, response.text
            )
        )

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

    def enroll_user_in_course(self, username, course_key_string):
        """
        Enroll the user in the course with the given key.

        Arguments:
            username (unicode): Username of the user to be enrolled.
            course_key_string (unicode): String version of the key of the
                course to enroll the user in.

        Raises:
            IOError if the user creation fails.
        """
        response = self.client.post(
            url=u"{}/enrollment".format(ENROLLMENT_API_BASE_URL),
            data=json.dumps({'course_details': {'course_id': course_key_string}}),
            headers=self._post_headers,
            verify=False,
            name=_get_current_function_name()
        )
        if response.status_code == 200:
            log("Enrolled user {} in course {}", username, course_key_string)
        else:
            log_error(
                "Failed to enroll user {} in course {}. Response status code = {}",
                username,
                course_key_string,
                response.status_code
            )

    def query_user_course_enrollments_list(self, username):  # pylint: disable=invalid-name
        """
        Query the UserCourseEnrollmentsList endpoint of the Mobile API for a
        particular user.

        Arguments:
            username (unicode): User name.
        """
        response = self.client.get(
            url=u"{}/users/{}/course_enrollments/?format=json".format(
                MOBILE_API_BASE_URL,
                username
            ),
            verify=False,
            name=_get_current_function_name()
        )
        if response.status_code != 200:
            log_error(
                "{} response for user {} returned status code {}",
                _get_current_function_name(),
                username,
                response.status_code
            )

    def query_student_dashboard(self, username):
        """
        Query the student dashboard.

        Arguments:
            username (unicode): User name.
        """
        response = self.client.get(
            url=DASHBOARD_BASE_URL,
            verify=False,
            name=_get_current_function_name()
        )
        if response.status_code != 200:
            log_error(
                "{} response for user {} returned status code {}",
                _get_current_function_name(),
                username,
                response.status_code
            )


def _load_course_pool_keys():
    """
    Load up the course keys to use in this test.

    Procedure:
        - Load courses from all-courses.json.
        - Deterministically shuffle keys based on RANDOM_GEN_SEED
        - Separate into Draft course keys and Split course keys
        - Filter out BAD_{DRAFT,SPLIT}_COURSE_KEYS
        - Return two lists of equal size (COURSE_POOL_SIZE - num_bad_keys),
          one containing Draft keys and the other containing Split keys.

    Returns:
        (list[str], list[str]): Two lists containing strings of the Mongo
            Draft and Split course keys, respectively, to be used in this
            test.
    """
    # Load courses from all-courses.json.
    with open("all-courses.json", 'r') as courses_json_file:
        courses = json.load(courses_json_file)['results']

    # Deterministically shuffle the course keys based on RANDOM_GEN_SEED.
    random_gen = random.Random()
    random_gen.seed(RANDOM_GEN_SEED)
    random.shuffle(courses, random_gen.random)

    # Separate into Draft course keys and Split course keys.
    course_keys = [
        (course['id'], course['id'].startswith('course-'))
        for course in courses
    ]
    draft_keys, split_keys = (
        [
            course_key for course_key, is_split in course_keys
            if not is_split
            and course_key not in BAD_DRAFT_COURSE_KEYS
        ],
        [
            course_key for course_key, is_split in course_keys
            if is_split
            and course_key not in BAD_SPLIT_COURSE_KEYS
        ],
    )

    # We use different sets of courses for development vs. actually
    # performing the test because we want to avoid warming up the
    # CourseOverview cache before the real test starts.
    num_bad_keys = max(len(BAD_DRAFT_COURSE_KEYS), len(BAD_SPLIT_COURSE_KEYS))
    if DEVELOPER_MODE:
        start_index = COURSE_POOL_SIZE - num_bad_keys
        end_index = start_index + DEV_COURSE_POOL_SIZE
    else:
        start_index = 0
        end_index = COURSE_POOL_SIZE - num_bad_keys
    return draft_keys[start_index:end_index], split_keys[start_index:end_index]


class CourseEnrollmentTaskSet(locust.TaskSet):
    """
    Task set for a single locust.
    """

    _draft_pool_keys, _split_pool_keys = _load_course_pool_keys()
    _generate_user_number = itertools.count().next

    @staticmethod
    def _get_random_course_key_set(user_number):
        """
        Generates a pseudo-random set of course keys.

        Course.draft_courses_per_user courses are selected from a pool
        of Course.(dev_)?course_pool_size draft courses.

        Course.split_courses_per_user courses are selected from a pool
        of Course.(dev_)?course_pool_size split courses.

        The random number generator is seeded with user_number, so given the
        same user number, the same set of course keys will be returned. This is
        by design in order to allow the load test to be repeatable.

        Returns:
            list[str]: Pseudo-random list of course keys.
        """

        # Seed the random number generator based on:
        #   (a) the test-wide seed, and
        #   (b) the user-specific seed.
        random_gen = random.Random()
        random_gen.seed(RANDOM_GEN_SEED * 2000 + user_number)

        pool_size = len(CourseEnrollmentTaskSet._draft_pool_keys)

        available_draft_indices = range(pool_size)
        random_draft_indices = [
            available_draft_indices.pop(random_gen.randrange(len(available_draft_indices)))
            for _ in range(DRAFT_COURSES_PER_USER)
        ]
        available_split_indices = range(pool_size)
        random_split_indices = [
            available_split_indices.pop(random_gen.randrange(len(available_split_indices)))
            for _ in range(SPLIT_COURSES_PER_USER)
        ]

        return (
            [CourseEnrollmentTaskSet._draft_pool_keys[i] for i in random_draft_indices] +
            [CourseEnrollmentTaskSet._split_pool_keys[i] for i in random_split_indices]
        )

    def __init__(self, *args, **kwargs):
        super(CourseEnrollmentTaskSet, self).__init__(*args, **kwargs)
        self.user_number = CourseEnrollmentTaskSet._generate_user_number()
        self.username = None
        self.api = TestApi(self.locust.host, self.client)

    def on_start(self):
        """
        Initialization to be performed by each locust before it begins to swarm.

        Create new user and enroll them in random courses.
        """
        self.username = self.api.create_and_log_in_user(is_staff=True)
        course_keys_strings = CourseEnrollmentTaskSet._get_random_course_key_set(self.user_number)
        for course_key_string in course_keys_strings:
            self.api.enroll_user_in_course(self.username, course_key_string)

    @locust.task(1 if ENDPOINT_TO_TEST == 'user_course_enrollments_list' else 0)
    def query_user_course_enrollments_list(self):  # pylint: disable=invalid-name
        """
        Query the Mobile API's UserCourseEnrollmentList endpoint once.
        """
        self.api.query_user_course_enrollments_list(self.username)

    @locust.task(1 if ENDPOINT_TO_TEST == 'student_dashboard' else 0)
    def query_student_dashboard(self):
        """
        Query the LMS student dashboard once.
        """
        self.api.query_student_dashboard(self.username)


class CourseEnrollmentTestUser(locust.HttpLocust):  # pylint: disable=too-few-public-methods
    """
    A single 'locust' in the swarm.
    """
    task_set = CourseEnrollmentTaskSet
    min_wait = max_wait = USER_WAIT_MS_PER_QUERY
