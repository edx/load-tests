import csv
import random
from timeit import default_timer
from locust import task, TaskSet
from locust.exception import StopLocust
from config import INSTRUCTOR_PACED_COURSE_KEYS, COURSE_URL_PREFIX, USER_CREDENTIALS
from certificates import Certificates
from auto_auth_tasks import AutoAuthTasks


class InstructorPacedCoursePage(Certificates):
    """
    Base class for page objects.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(InstructorPacedCoursePage, self).__init__(*args, **kwargs)

    def generate_certificate(self, course_key):
        """
        Generate the certificate from staff login
        :param course_key:
        """
        course_info_url = COURSE_URL_PREFIX + course_key + u"/info"
        self._get(course_info_url)
        # Go to instructor tab
        staff_view_url = COURSE_URL_PREFIX + course_key + u"/instructor"
        self._get(staff_view_url)
        # Generate the certificate
        generate_certificate_url = COURSE_URL_PREFIX + course_key + u"/instructor/api/start_certificate_generation"
        self._post(generate_certificate_url)


class InstructorPacedCreateStudents(AutoAuthTasks):
    """
    User scripts that creates students and make them eligible for certificates.
    Information about these users is recorded in a csv file so it can be used in later scripts
    """

    def __init__(self, *args, **kwargs):
        """\
        Initialize the Task set.
        """
        super(InstructorPacedCreateStudents, self).__init__(*args, **kwargs)
        self.page = InstructorPacedCoursePage(self.locust.host, self.client)

    @task
    def create_eligible_students(self):
        """
        This task is basically used for creating the data and there is no need to measure time
        for it. Here are the steps covered in this task
        1) login to application using auto auth
        2) Enroll for the course
        3) Save the Credentials like user_id, user_name, email and course_key in a csv file(This is done
        so that same credentials can be used afterwards in different tasks for viewing the certificate)
        4) Attempt the first exercise with correct answer to make sure that each user qualifies for
        the certificate
        5) Implemented a time based restrain on the task so that it stops after reasonable data is generated.
        """
        start = default_timer()
        for course_key in INSTRUCTOR_PACED_COURSE_KEYS:
            # Login to application using auto auth as a student
            self.auto_auth()
            # Enroll for the target self paced course
            self.page.enroll(course_key)
            # Attempt first mcq to become eligible for certificate
            self.page.attempt_exercise(course_key)
            # Logout as student
            self.page.logout()
            # Log the students' credential in a csv so these can be used in 3rd task
            with open('credentials.csv', 'a') as csv_write_file:
                csv_writer = csv.writer(csv_write_file)
                csv_writer.writerow([self._user_id, self._username, course_key])
        # Stop the task after running for some minutes
        duration = default_timer() - start
        if duration > 50:
            raise StopLocust


class InstructorPacedGenerateCertificates(AutoAuthTasks):
    """
    User scripts that generates the certificates using instructor dashboard.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(InstructorPacedGenerateCertificates, self).__init__(*args, **kwargs)
        self.page = InstructorPacedCoursePage(self.locust.host, self.client)

    @task
    def generate_certificate_as_staff(self):
        """
        Use the list of courses to generate certificates against each course. The restraint on the instructor
        side is that we cannot run multiple tasks of certificate generation for one course at the same time. Also
        generating a certificate again for same course would not do anything unless more data has been added. So we
        have retrained the task to run only once for all course, once the certificates are generated for all course
        the script will stop the Locusts
        """
        if INSTRUCTOR_PACED_COURSE_KEYS:
            course_key = INSTRUCTOR_PACED_COURSE_KEYS.pop()
            # Login to application using auto auth as a staff
            self.auto_auth(params={"staff": "true"})
            # Enroll to course as a staff
            self.page.enroll(course_key)
            # generate a certificate
            self.page.generate_certificate(course_key)
            # Logout
            self.page.logout()
        # Stop the locust when certificates are generated for all courses
        else:
            raise StopLocust


class InstructorPacedViewCertificatesTask(TaskSet):
    """
    User scripts that tests viewing of certificates by students which are created in above class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(InstructorPacedViewCertificatesTask, self).__init__(*args, **kwargs)
        self.page = InstructorPacedCoursePage(self.locust.host, self.client)

    @task
    def view_certificate(self):
        """
        Fetch some random credentials for the csv that was generated in CreateStudentTask. Repeatedly view the
        certificate for these users
        """
        self.page = InstructorPacedCoursePage(self.locust.host, self.client)
        credentials = random.choice(USER_CREDENTIALS)
        user_id = credentials[0]
        user_name = credentials[1]
        course_key = credentials[2]
        # view the certificate for the selected user
        self.page.query_certificate(user_id, user_name, course_key)
