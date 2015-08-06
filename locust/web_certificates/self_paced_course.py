import random
from locust import task
from config import SELF_PACED_COURSE_KEYS, COURSE_URL_PREFIX
from certificates import Certificates
from auto_auth_tasks import AutoAuthTasks


class SelfPacedCoursePage(Certificates):
    """
    Base class for page objects.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(SelfPacedCoursePage, self).__init__(*args, **kwargs)

    def request_certificate(self, course_key):
        """
        Generate a certificate by going to progress page and submitting Request certificate command
        :param course_key:
        """
        progress_url = COURSE_URL_PREFIX + course_key + u"/progress"
        self._get(progress_url, verify_response_string="Congratulations")
        # verify that you are eligible for certificate
        # request certificate generation
        certificate_request_url = COURSE_URL_PREFIX + course_key + u"/generate_user_cert"
        self._post(certificate_request_url)


class SelfPacedCompleteTask(AutoAuthTasks):
    """
    User scripts that exercise the web certificate viewing feature for self paced course.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(SelfPacedCompleteTask, self).__init__(*args, **kwargs)
        self.page = SelfPacedCoursePage(self.locust.host, self.client)
        self.course_key = ""

    def on_start(self):
        """
        Login with a new user and request a certificate, auto_ath functionality is used to login with new users,
        these users are then enrolled in course and each student will attempt a pre defined exercise to become
        eligible for certificate. After the attempt user will go to progress page and request for the certificate.
        """
        self.course_key = random.choice(SELF_PACED_COURSE_KEYS)
        self.auto_auth()
        # Enroll for the target self paced course
        self.page.enroll(self.course_key)
        # Attempt first mcq to become eligible for certificate
        self.page.attempt_exercise(self.course_key)
        # make a request for a certificate
        self.page.request_certificate(self.course_key)

    @task
    def view_certificates(self):
        """
        View the web certificate repeatedly for all users
        """
        self.page.query_certificate(
            self._user_id,
            self._username,
            self.course_key,
            group_url_name="/view_student_certificate_url"
        )
