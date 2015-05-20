import os
import re
from locust import task, TaskSet


BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (
        os.environ['BASIC_AUTH_USER'],
        os.environ['BASIC_AUTH_PASSWORD']
    )


class AutoAuthTasks(TaskSet):
    """
    Methods useful to any/all tests that want to use auto auth.
    """

    def __init__(self, *args, **kwargs):
        """
        Add basic auth credentials to our client object when specified.
        """
        super(AutoAuthTasks, self).__init__(*args, **kwargs)
        if BASIC_AUTH_CREDENTIALS:
            self.client.auth = BASIC_AUTH_CREDENTIALS

        self._user_id = None
        self._anonymous_user_id = None
        self._username = None
        self._email = None
        self._password = None

    def auto_auth(self):
        """
        Logs in with a new, programmatically-generated user account.
        Requires AUTO_AUTH functionality to be enabled in the target edx instance.
        """
        if "sessionid" in self.client.cookies:
            del self.client.cookies["sessionid"]

        response = self.client.get("/auto_auth", name="auto_auth")
        match = re.search(
            r'Logged in user ([\w]+) \(([\w@\.]+)\) with password ([\w]+) and user_id ([\d]+) and anonymous user_id ([\w]+)',
            response.text
        )
        self._username, self._email, self._password, self._user_id, self._anonymous_user_id = match.groups()

    @task
    def stop(self):
        """
        Supports usage as nested or top-level task set.
        """
        if self.parent != self.locust:
            self.interrupt()
