"""
Load test for the edx-platform user API.

Usage:

  $ locust --host="http://localhost:8000"

Supported Environment Variables:

  BASIC_AUTH_USER, BASIC_AUTH_PASS - if set, will use for HTTP Authentication
  LOCUST_TASK_SET - if set, will run the specified TaskSet (must be imported in this module)
  LOCUST_MIN_WAIT, LOCUST_MAX_WAIT - use to override defaults set in this module

"""

import os

from user_api import UserAPITasks
from accounts import AccountsTasks
from preferences import PreferencesTasks
from profile_images import ProfileImagesTasks

from locust import HttpLocust


class UserAPITest(UserAPITasks):
    tasks = {
        AccountsTasks: 3,
        ProfileImagesTasks: 2,
        PreferencesTasks: 1,
    }


class UserAPILocust(HttpLocust):
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'UserAPITest')]
    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 7500))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 15000))
