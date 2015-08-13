"""
Load tests for the courseware student module.
"""

import os
import random
import sys
import time

from locust import Locust, TaskSet, task, events

# Work around the fact that Locust runs locustfiles as scripts within packages
# and therefore doesn't allow the use of absolute or explicit relative imports.

sys.path.append("/home/alawi/edx/orphans/edx-platform/lms")
sys.path.append("/home/alawi/edx/orphans/edx-platform/lms/djangoapps")
sys.path.append("/home/alawi/edx/orphans/edx-platform/common/djangoapps")
sys.path.append("/home/alawi/bin/opaque-keys/")

from opaque_keys.edx.locator import BlockUsageLocator

os.environ["DJANGO_SETTINGS_MODULE"] = "lms.envs.devplus"

class QuestionResponse(TaskSet):
    "Respond to a question in the LMS."

    @task
    def set_many(self):
        "set many load test"

        usage = BlockUsageLocator.from_string('block-v1:HarvardX+SPU27x+2015_Q2+type@html+block@1a1866accf254461aa2df3e0b4238a5f')
        start_time = time.time()
        try:
            self.client.set_many(self.client.user.username, {usage: {"soup": "delicious"}})
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="", name="set_many", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="", name="set_many", response_time=total_time, response_length=0)

    @task
    def get_many(self):
        "get many load test"

        usage = BlockUsageLocator.from_string('block-v1:HarvardX+SPU27x+2015_Q2+type@html+block@1a1866accf254461aa2df3e0b4238a5f')
        start_time = time.time()
        try:
            [s for s in self.client.get_many(self.client.user.username, [usage])]
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="", name="get_many", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="", name="get_many", response_time=total_time, response_length=0)

class UserStateClientClient(Locust):
    "Locust class for the User State Client."

    task_set = QuestionResponse
    min_wait = 1000
    max_wait = 5000

    def __init__(self):
        super(UserStateClientClient, self).__init__()
        if self.host is None:
            raise LocustError("You must specify the base host. Either in the host attribute in the Locust class, or on the command line using the --host option.")

        from django.conf import settings
        settings.DATABASES = {
                'default': {
                'HOST': self.host,
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'edxapp',
                'USER': 'edxapp',
                'PASSWORD': 'password',
                'PORT': '3306',
            }
        }
        import courseware.user_state_client as user_state_client
        from student.tests.factories import UserFactory

        self.client = user_state_client.DjangoXBlockUserStateClient(user=UserFactory.create())
