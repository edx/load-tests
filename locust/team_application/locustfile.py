"""
Load test for the Team API as used by the edX application.

Usage:

  $ locust --host="http://localhost:8000"

Supported Environment Variables:

  BASIC_AUTH_USER, BASIC_AUTH_PASS - if set, will use for HTTP Authentication
  LOCUST_TASK_SET - if set, will run the specified TaskSet (must be imported in this module)
  LOCUST_MIN_WAIT, LOCUST_MAX_WAIT - use to override defaults set in this module
  COURSE_ID - course that will be tested on the target host, default is set in lms.LmsTasks
  STUDIO_HOST - the URL where Studio is running, default set to http://localhost:8001.

"""
from locust import task, HttpLocust
import os
import random
import sys

# Workaround for Locust running locustfiles as scripts instead of real
# packages.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'team_api'))
from team_api import BaseTeamsTask


class TeamAppTasks(BaseTeamsTask):
    """ Tasks to exercise Teams API endpoints as used by the edX application. """
    @task(2)
    def teams_dashboard(self):
        self._get_dashboard()

    @task(3)
    def create_team(self):
        self._create_team()

    @task(1)
    def update_team(self):
        self._update_team()

    @task(20)
    def list_teams_for_topic(self):
        order_by = random.choice(['last_activity_at', 'open_slots'])
        topic_id = random.choice(self.topics)['id']
        self._list_teams({'topic_id': topic_id, 'order_by': order_by, 'expand': 'user'})

    @task(10)
    def list_teams_in_topic_search(self):
        query_string = self._get_search_query_string()
        topic_id = random.choice(self.topics)['id']
        self._list_teams({'topic_id': topic_id, 'text_search': query_string})

    @task(200)
    def team_detail(self):
        self._team_detail({'expand': 'user'})

    @task(20)
    def list_topics(self):
        self._list_topics()

    @task(20)
    def topic_detail(self):
        self._topic_detail()

    @task(20)
    def list_memberships_for_team_expand_user_and_team(self):
        self.team = self._get_top_name_team()
        self._list_memberships({'team_id': self.team['id'], 'expand': 'user,team'})

    @task(10)
    def change_membership(self):
        self._change_membership()

    @task(1)
    def delete_membership(self):
        self._delete_membership()

    @task(1)
    def stop(self):
        self._stop()


class TeamLocust(HttpLocust):
    """
    Wait times were chosen using this formula to find an average, then +/- 20%
    desired requests per sec = (number of users) * 1000 / (average wait in ms)

    The assumed values are 15 rps = 100 * 1000 / 6667.
    If more or less than 100 users are desired, scale the wait time by the same
    factor to hold the rps steady, or choose a different factor if changing rps

    These numbers were chosen to be roughly double the daytime throughput of
    Forums (450 rpm = 7.5 rps), as reported on New Relic for prod-edx-forum.
    """
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'TeamAppTasks')]

    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 5333))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 8000))
