import json
import itertools
import os
import re
import urllib

from locust import HttpLocust, task, TaskSet



COURSES_CYCLE_OLD = itertools.cycle([
    'edX/DemoX.1/2014',
    'course-v1:edX+DemoX.1+split',
    'MITx/6.002x/2013_Spring',
    'course-v1:MITx+6.002x+2013',
])

COURSES_CYCLE_NEW = itertools.cycle([
    'edX/DemoX.1/2014',
    'course-v1:edX+DemoX.1+split',
    'MITx/6.002x/2013_Spring',
    'course-v1:MITx+6.002x+2013',
])


class CoursesApiTaskSet(TaskSet):

    def __init__(self, *args, **kwargs):
        super(CoursesApiTaskSet, self).__init__(*args, **kwargs)
        self.username = None

    def on_start(self):
        self.auto_auth(staff="true")
        # self.enroll() # Seems like some of the samples used are not allowing students to enroll

    def auto_auth(self, staff="false"):
        response = self.client.get(
            url=u"/auto_auth",
            params={u'staff': staff},
            name="create_user"
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
        for course in COURSES_LIST:
            response = self.client.post(
                url=u"/api/enrollment/v1/enrollment",
                data=json.dumps({'course_details': {'course_id': course}}),
                headers=self._post_headers,
                verify=False,
                name="enroll {}".format(course)
            )
            if response.status_code == 200:
                print "Enrolled user {} in course {}".format(self.username, course)
            else:
                print ("Failed to enroll user {} in course {}. Response status code = {}".format(
                    self.username,
                    course,
                    response.status_code
                ))


class OldApiTask(CoursesApiTaskSet):
    @task
    def query_course(self):
        course_id = COURSES_CYCLE_OLD.next()
        url = u"/api/course_structure/v0/courses/{}/blocks+navigation".format(course_id)
        response = self.client.get(
            url=url,
            verify=False,
            name="GET_{},_using_the_{}".format(course_id, "Old_API")
        )
        if response.status_code != 200:
            print "ERROR: GET {} failed with status code {}".format(
                url,
                response.status_code
            )


class NewApiTask(CoursesApiTaskSet):
    @task
    def query_course(self):
        original_course_id =COURSES_CYCLE_NEW.next()
        course_id = urllib.quote_plus(original_course_id)
        base_url = u"/api/courses/v1/blocks"
        user = u"user={}".format(self.username.split(" ")[0])
        other_fields = u"depth=all&requested_fields=graded&requested_fields=format&requested_fields=student_view_multi_device&block_counts=video&student_view_data=video"
        course = u"course_id={}".format(course_id)

        url = u"{}/?{}&{}&{}".format(base_url, user, other_fields, course)
        response = self.client.get(
            url=url,
            verify=False,
            name="GET_{},_using_the_{}".format(original_course_id, "New_API")
        )
        if response.status_code != 200:
            print "ERROR: GET {} failed with status code {}".format(
                url,
                response.status_code
            )


class CoursesApiTests(CoursesApiTaskSet):

    tasks = {
        OldApiTask: 1,
        NewApiTask: 1
    }


class CoursesApiTestUser(HttpLocust):  # pylint: disable=too-few-public-methods
    """
    A single 'locust' in the swarm.
    """
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'CoursesApiTests')]
    min_wait = max_wait = 1000
