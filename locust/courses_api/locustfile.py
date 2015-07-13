import json
import locust
import os
import re


COURSES = {
    'demo_draft': 'edX/DemoX.1/2014',
    'demo_split': 'course-v1:edX+DemoX.1+LT_SPLIT',
    '6.002x_draft': 'MITx/6.002x/2013_Spring',
    '6.002x_split': 'course-v1:MITx+6.002x_6x+1T2015',
}
COURSE_KEY = COURSES.get(os.environ.get('COURSE', None), None)
if not COURSE_KEY:
    raise ValueError("COURSE must be one of: " + ", ".join(COURSES.keys()))

RESOURCES = [
    ''
    'blocks',
    'navigation',
    'blocks+navigation'
]
RESOURCE = os.environ.get('RESOURCE', None)
if RESOURCE not in RESOURCES:
    raise ValueError("RESOURCE must be one of: " + ", ".join(RESOURCES))


class CoursesApiTaskSet(locust.TaskSet):

    def __init__(self, *args, **kwargs):
        super(CoursesApiTaskSet, self).__init__(*args, **kwargs)
        self.username = None

    def on_start(self):
        self.auto_auth()
        self.enroll()

    def auto_auth(self):
        response = self.client.get(
            url=u"/auto_auth",
            params={u'staff': u"true"},
            name="create user"
        )
        if response.status_code == 200:
            match = re.search(r'(Logged in|Created) user (?P<username>[^$]+).*', response.text)
            if match:
                self.username = match.group('username')
                print "Successfully created and logged in user {}".format(self.username)
        else:
            raise IOError(
                "Failed to authorize user. Response (status {}): {}".format(
                    response.status_code, response.text
                )
            )

    @property
    def _post_headers(self):
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host
        }

    def enroll(self):
        response = self.client.post(
            url=u"/api/enrollment/v1/enrollment",
            data=json.dumps({'course_details': {'course_id': COURSE_KEY}}),
            headers=self._post_headers,
            verify=False,
            name="enroll {}".format(COURSE_KEY)
        )
        if response.status_code == 200:
            print "Enrolled user {} in course {}".format(self.username, COURSE_KEY)
        else:
            print ("Failed to enroll user {} in course {}. Response status code = {}".format(
                self.username,
                COURSE_KEY,
                response.status_code
            ))

    @locust.task
    def query_course(self):
        url = u"/api/course_structure/v0/courses/{}/{}".format(COURSE_KEY, RESOURCE)
        response = self.client.get(
            url=url,
            verify=False,
            name="get courses/{}/{}".format(COURSE_KEY, RESOURCE)
        )
        if response.status_code != 200:
            print "ERROR: GET {} failed with status code {}".format(
                url,
                response.status_code
            )


class CoursesApiTestUser(locust.HttpLocust):  # pylint: disable=too-few-public-methods
    """
    A single 'locust' in the swarm.
    """
    task_set = CoursesApiTaskSet
    min_wait = max_wait = 1000
