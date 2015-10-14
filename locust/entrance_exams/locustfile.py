"""
Performance tests for Entrance exams.

To start the test server on the host "www.example.com":

$ BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password locust --host https://www.example.com

Then visit http://127.0.0.1:8089

You can omit basic auth credentials if the test server is not protected by basic auth.

The optional environment variable LOCUST_TASK_SET is used run an individual task, test will
run for all tasks of courses by default

TASK_TYPE=PreEntrance will run the Student Task for course with Entrance Exam without passing it
TASK_TYPE=PostEntrance will run the Student Task for course with Entrance Exam after it is passed
TASK_TYPE=Simple will run the Student Task for a simple course without Entrance Exam
Not using the TASK_TYPE will result in running the Instructor task
"""
from config import TASK_TYPE
from locust import HttpLocust
from tasks import (
    EntranceExamStudentTasks,
    EntranceExamInstructorTasks
)


class EntranceExamLocust(HttpLocust):
    """
    Representation of an HTTP "user".
    Defines how long a simulated user should wait between executing tasks, as
    well as which TaskSet class should define the user's behavior.
    """
    if TASK_TYPE == '':
        task_set = EntranceExamInstructorTasks
    else:
        task_set = EntranceExamStudentTasks
    min_wait = 3000
    max_wait = 6000
