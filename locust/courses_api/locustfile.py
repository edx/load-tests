"""
Load tests for the course_overviews course metadata caching framework.

Environment variables:

    ENDPOINT_TO_TEST
        ...

    BASIC_AUTH
        Format: username,password
        Specifies the basic auth credentials for the target server.
        Optional; defaults to no basic auth.

    LOGGING_LEVEL
        Values: none, error, all
        How much logging output to display.
        Optional; defaults to error.

How the test works:
    ...
"""

import locust
import os


# Logging levels
LOG_NONE = 0
LOG_ERROR = 1
LOG_ALL = 2

# Environment variable options; initialized in init_environment_variables
ENDPOINT_TO_TEST = None
BASIC_AUTH = None


def init_environment_variables():
    """
    Initializes configuration options from environment variables.

    Should be called exactly once near the beginning of the test.
    """
    global ENDPOINT_TO_TEST, BASIC_AUTH, LOGGING_LEVEL  # pylint: disable=global-statement

    # TODO
    '''
    valid_test_endpoints = ['user_course_enrollments_list', 'student_dashboard']
    ENDPOINT_TO_TEST = os.environ.get('ENDPOINT_TO_TEST', None)
    if ENDPOINT_TO_TEST not in valid_test_endpoints:
        raise Exception(
            "Must specify ENDPOINT_TO_TEST as one of: " +
            ", ".join(valid_test_endpoints)
        )
    '''

    basic_auth_string = os.environ.get('BASIC_AUTH', None)
    BASIC_AUTH = tuple(basic_auth_string.split(',')) if basic_auth_string else None

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
    Class for interacting with the different endpoints that we'll be testing.
    """

    COURSES_BASE_URL = u"/api/courses/v1"
    INSTRUCTORS_BASE_URL = u"/api/instructors/v1"

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

    def student_query_all_courses(self):
        """
        Query metadata for all courses the user can view as a student.

        /api/courses/v1/courses/
        """
        query_url = u"{}/courses".format(TestApi.COURSES_BASE_URL)
        response = self.client.get(
            name=u"Courses API: courses",
            url=query_url,
            verify=False
        )
        if response.status_code != 200:
            log_error(u"{} returned status {}".format(query_url, response.status_code))

    def student_query_course(self, course_key_string, resource):
        """
        Make a course-specific query as student.

        /api/courses/v1/courses/{course_key}/{resource}

        Arguments:
            course_key_string (str): String of the key of the course to query.
            resource (str): One of the following:
                ""                  -> course metadata
                "blocks"            -> user-specific course XBlocks
                "navigation"        -> user-specific course navigation structure
                "blocks+navigation" -> user-specific course XBlocks AND
                                       navigation structure
        """
        query_url = u"{}/courses/{}/{}".format(TestApi.COURSES_BASE_URL, course_key_string, resource)
        response = self.client.get(
            name=u"Courses API: courses/<course_key>/{}".format(resource),
            url=query_url,
            verify=False
        )
        if response.status_code != 200:
            log_error(u"{} returned status {}".format(query_url, response.status_code))

    def instructor_query_all_courses(self):
        """
        Query metadata for all courses for which the user is an instructor.

        /api/instructors/v1/courses/
        """
        query_url = u"{}/courses".format(TestApi.INSTRUCTORS_BASE_URL)
        response = self.client.get(
            name=u"Instructors API: courses",
            url=query_url,
            verify=False
        )
        if response.status_code != 200:
            log_error(u"{} returned status {}".format(query_url, response.status_code))

    def instructor_query_course(self, course_key_string, resource):
        """
        Make a course-specific query as an instructor.

        /api/instructors/v1/courses/{course_key}/{resource}

        Arguments:
            course_key_string (str): String of the key of the course to query.
            resource (str): One of the following:
                "blocks"            -> all course XBlocks
                "grading-policy"    -> course grading policy
        """
        query_url = u"{}/courses/{}/{}".format(TestApi.INSTRUCTORS_BASE_URL, course_key_string, resource)
        response = self.client.get(
            name=u"Instructors API: courses",
            url=query_url,
            verify=False
        )
        if response.status_code != 200:
            log_error(u"{} returned status {}".format(query_url, response.status_code))


class CoursesApiTaskSet(locust.TaskSet):



class CoursesApiTestUser(locust.HttpLocust):  # pylint: disable=too-few-public-methods
    """
    A single 'locust' in the swarm.
    """
    task_set = CoursesApiTaskSet
    # TODO min_wait = max_wait = USER_WAIT_MS_PER_QUERY