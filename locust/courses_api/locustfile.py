
import locust
import os
import re


COURSE_KEY = os.environ['COURSE_KEY']


class CoursesApiTaskSet(locust.TaskSet):

    def on_start(self):
        response = self.client.get(
            url=u"/auto_auth",
            params={u'staff': u"True"},
            name="create user"
        )
        if response.status_code == 200:
            match = re.search(r'(Logged in|Created) user (?P<username>[^$]+).*', response.text)
            if match:
                username = match.group('username')
                print "Successfully created and logged in user {}".format(username)
        raise IOError(
            "Failed to authorize user. Response (status {}): {}".format(
                response.status_code, response.text
            )
        )

    @locust.task
    def query_course(self):
        response = self.client.get(
            url=u"/api/course_structure_api/v0/courses/{}/blocks+navigation".format(COURSE_KEY),
            verify=False,
            name="get {}".format(COURSE_KEY)
        )
        if response.status_code != 200:
            print "ERROR: Query failed with status code {}".format(response.status_code)


class CoursesApiTestUser(locust.HttpLocust):  # pylint: disable=too-few-public-methods
    """
    A single 'locust' in the swarm.
    """
    task_set = CoursesApiTaskSet
    min_wait = max_wait = 1000
