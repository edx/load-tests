from locust import task
from config import COURSES, TASK_TYPE
from pages import ExamPage, InstructorPage
from auto_auth_tasks import AutoAuthTasks


class EntranceExamStudentTasks(AutoAuthTasks):
    """
    User scripts to run Tasks related to entrance Exams before passing.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(EntranceExamStudentTasks, self).__init__(*args, **kwargs)
        self.page = ExamPage(self.locust.host, self.client)

    def on_start(self):
        """
        create a new user using auto auth functionality,
        enroll this user to entrance exam course
        """
        course = COURSES[TASK_TYPE]
        self.course_id = course['course_id']
        self.exam_name = course['exam_name']
        self.coursware_link = course['coursware_link']
        self.exam_link = course['exam_link']
        self.input_choice = course['input_choice']
        self.input_choice_type = course['input_choice_type']
        self.auto_auth(params={'course_id': self.course_id})
        # fetch the exam url from course ware source code
        self.exam_url = self.page.fetch_exam_url(
            self.course_id,
            self.exam_name,
            self.coursware_link
        )
        # attempt the entrance exam once in case of post entrance exam task
        if TASK_TYPE == 'post-entrance':
            self.page.exam_attempt(
                self.course_id,
                self.exam_url,
                self.input_choice,
                self.input_choice_type,
                '[EntranceExam Initial State Exam Page]'
            )

    @task
    def load_courseware_page(self):
        """
        load courseware repeatedly
        """
        self.page.load_courseware(self.course_id, self.coursware_link)

    @task
    def load_exam_page(self):
        """
        load exam page repeatedly
        """
        self.page.load_exam(self.exam_url, self.exam_link)

    @task
    def attempt_exam(self):
        """
        attempt entrance exam repeatedly
        """
        self.page.exam_attempt(
            self.course_id,
            self.exam_url,
            self.input_choice,
            self.input_choice_type,
            self.exam_link
        )


class EntranceExamInstructorTasks(AutoAuthTasks):
    """
    User scripts to run the Instructor tasks for Entrance Exam
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(EntranceExamInstructorTasks, self).__init__(*args, **kwargs)
        self.exam_page = ExamPage(self.locust.host, self.client)
        self.instructor_page = InstructorPage(self.locust.host, self.client)

    def on_start(self):
        """
        create a new user using auto auth functionality,
        enroll this user to entrance exam course
        attempt the entrance exam to make sure that all course content is unlocked
        Record the student user name in a variable
        Now create a staff user using auto auth and enroll to the same course
        """
        course = COURSES['post-entrance']
        self.course_id = course['course_id']
        self.exam_name = course['exam_name']
        self.coursware_link = course['coursware_link']
        self.exam_link = course['exam_link']
        self.input_choice = course['input_choice']
        self.input_choice_type = course['input_choice_type']
        self.auto_auth(params={'course_id': self.course_id})
        self.student_username = self._username
        # fetch the exam url from course ware source code
        self.exam_url = self.exam_page.fetch_exam_url(
            self.course_id,
            self.exam_name,
            self.coursware_link
        )
        # attempt the entrance exam with correct choice
        self.exam_page.exam_attempt(
            self.course_id,
            self.exam_url,
            self.input_choice,
            self.input_choice_type,
            '[EntranceExam Initial State Exam Page]'
        )
        self.auto_auth(params={'course_id': self.course_id, 'staff': 'true'})
        self.action_api_url = self.instructor_page.go_to_instructor_dashboard(self.course_id)

    @task
    def reset_student_attempt(self):
        """
        Reset Student attempt from instructor dashboard
        """
        self.instructor_page.reset_attempt(self.student_username, self.action_api_url)

    @task
    def rescore_student_exam(self):
        """
        Rescore Student exam from instructor dashboard
        """
        self.instructor_page.rescore_exam(self.student_username, self.action_api_url)

    @task
    def delete_student_attempt(self):
        """
        Delete Student attempt from instructor dashboard
        """
        self.instructor_page.delete_attempt(self.student_username, self.action_api_url)

    @task
    def skip_student_exam(self):
        """
        Skip Student exam from instructor dashboard
        """
        self.instructor_page.skip_exam(self.student_username, self.action_api_url)
