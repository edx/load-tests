"""
Comparative Performance tests for Proctored exams.

To start the test server on the host "www.example.com":

$ BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password locust --host https://www.example.com

Then visit http://127.0.0.1:8089

You can omit basic auth credentials if the test server is not protected by basic auth.

The optional environment variable LOCUST_TASK_SET is used run an individual task, test will
run for all tasks of courses by default

LOCUST_TASK_SET=ProctoredTasks will run the test for only Proctored course
LOCUST_TASK_SET=NonProctoredTasks will run the test for only Non Proctored course

"""
import os
from locust import HttpLocust, TaskSet
from exam_tasks import ProctoredTasks, NonProctoredTasks


class ProctoringTest(TaskSet):

    tasks = {
        ProctoredTasks: 1,
        NonProctoredTasks: 1
        }


class ProctoringLocust(HttpLocust):
    """
    Representation of an HTTP "user".
    Defines how long a simulated user should wait between executing tasks, as
    well as which TaskSet class should define the user's behavior.
    """
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'ProctoringTest')]
    min_wait = 500
    max_wait = 1000
