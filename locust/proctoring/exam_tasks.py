import random
from locust import task
from config import (
    PROCTORED_COURSES,
    NON_PROCTORED_COURSES
)
from exam_pages import ExamPages
from auto_auth_tasks import AutoAuthTasks


class ProctoredTasks(AutoAuthTasks):
    """
    User scripts that exercise the web certificate viewing feature for self paced course.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(ProctoredTasks, self).__init__(*args, **kwargs)
        self.page = ExamPages(self.locust.host, self.client)
        self.exam_info = []

    def on_start(self):
        """
        create a new user using auto auth functionality,
        enroll this user to proctored course
        Go to exm page and start a timed exam
        """
        course_info = random.choice(PROCTORED_COURSES.items())
        self.auto_auth(params={'course_id': course_info[0], 'enrollment_mode': 'verified'})
        # fetch the exam url from courseware source code
        self.exam_info = self.page.fetch_exam_url(course_info[0], course_info[1])
        exam_id = self.page.load_start_exam_screen(self.exam_info)
        self.page.start_exam(exam_id, self.exam_info)

    @task
    def load_exam(self):
        """
        load exam page using the exam url and exam name
        """
        self.page.load_exam(self.exam_info)


class NonProctoredTasks(AutoAuthTasks):
    """
    User scripts that exercise the web certificate viewing feature for self paced course.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(NonProctoredTasks, self).__init__(*args, **kwargs)
        self.page = ExamPages(self.locust.host, self.client)
        self.exam_info = []

    def on_start(self):
        """
        create a new user using auto auth functionality,
        enroll this user to non proctored course
        Fetch the exam url from courseware page source
        """
        course_info = random.choice(NON_PROCTORED_COURSES.items())
        self.auto_auth(params={'course_id': course_info[0]})
        # fetch the exam url from courseware source code
        self.exam_info = self.page.fetch_exam_url(course_info[0], course_info[1])

    @task
    def load_exam(self):
        """
        load exam page using the url and exam name
        """
        self.page.load_exam(self.exam_info)
