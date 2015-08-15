"""
Performance tests for enrollment API.

To start the test server on the host "www.example.com":

$ BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password TASK_NUM=0 locust --host https://www.example.com

Then visit http://127.0.0.1:8089

You can omit basic auth credentials if the test server is not protected by basic auth.

The environment variable TASK_NUM is used to make sure that we are running th intended Task
TASK_NUM=0 will run the Default test i.e. the SelfPaced CompleteTask
TASK_NUM=1 will run InstructorPacedCreateStudents task to create student
TASK_NUM=2 will run InstructorPacedGenerateCertificates task to generate certificates
TASK_NUM=3 will run InstructorPacedViewCertificatesTask to view instructor paced certificates
"""

import os
from locust import HttpLocust
from self_paced_course import SelfPacedCompleteTask
from instructor_paced_course import (
    InstructorPacedCreateStudents,
    InstructorPacedGenerateCertificates,
    InstructorPacedViewCertificatesTask
)

locust_tasks = [
    SelfPacedCompleteTask,
    InstructorPacedCreateStudents,
    InstructorPacedGenerateCertificates,
    InstructorPacedViewCertificatesTask
    ]


class CertificateLocust(HttpLocust):
    """
    Representation of an HTTP "user".
    Defines how long a simulated user should wait between executing tasks, as
    well as which TaskSet class should define the user's behavior.
    """
    task_num = int(os.getenv('TASK_NUM', 0))
    task_set = locust_tasks[task_num]
    min_wait = 500
    max_wait = 1000
