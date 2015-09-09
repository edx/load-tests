"""
Load test for the Team API.

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


class TeamAPITasks(BaseTeamsTask):
    """ Exercise Teams API endpoints. """

    # TEAMS
    # Create Teams
    @task(10)
    def create_team(self):
        self._create_team()

    # Update Teams
    @task(1)
    def update_team(self):
        self._update_team()

    # List Teams
    @task(20)
    def list_teams(self):
        self._list_teams()

    @task(20)
    def list_teams_expand_user(self):
        self._list_teams({'expand': 'user'})

    @task(20)
    def list_teams_expand_team(self):
        self._list_teams({'expand': 'team'})

    @task(20)
    def list_teams_expand_user_and_team(self):
        self._list_teams({'expand': 'user,team'})

    @task(20)
    def list_teams_for_topic(self):
        order_by = random.choice(['name', 'last_activity_at', 'open_slots'])
        topic_id = random.choice(self.topics)['id']
        self._list_teams({'topic_id': topic_id, 'order_by': order_by})

    @task(20)
    def list_teams_search(self):
        query_string = self._get_search_query_string()
        self._list_teams({'text_search': query_string})

    @task(20)
    def list_teams_in_topic_search(self):
        query_string = self._get_search_query_string()
        topic_id = random.choice(self.topics)['id']
        self._list_teams({'topic_id': topic_id, 'text_search': query_string})

    # Get Team Details
    @task(50)
    def team_detail(self):
        self._team_detail()

    @task(50)
    def team_detail_expands_user(self):
        self._team_detail({'expand': 'user'})

    @task(50)
    def team_detail_expands_team(self):
        self._team_detail({'expand': 'team'})

    @task(50)
    def team_detail_expands_user_and_team(self):
        self._team_detail({'expand': 'user,team'})

    # TOPICS
    # List topics
    @task(40)
    def list_topics(self):
        self._list_topics()

    # Get topic details
    @task(120)
    def topic_detail(self):
        self._topic_detail()

    # MEMBERSHIPS
    # Create/Update memberships
    @task(40)
    def create_or_change_membership(self):
        self._change_membership()

    # List Memberships
    @task(25)
    def list_memberships_for_user(self):
        self._list_memberships({'username': self._username})

    @task(25)
    def list_memberships_for_user_expand_user(self):
        self._list_memberships({'username': self._username, 'expand': 'user'})

    @task(25)
    def list_memberships_for_user_expand_team(self):
        self._list_memberships({'username': self._username, 'expand': 'team'})

    @task(25)
    def list_memberships_for_user_expand_user_and_team(self):
        self._list_memberships({'username': self._username, 'expand': 'user,team'})

    @task(25)
    def list_memberships_for_team(self):
        self.team = self._get_team()
        self._list_memberships({'team_id': self.team['id']})

    @task(25)
    def list_memberships_for_team_expand_user(self):
        self.team = self._get_team()
        self._list_memberships({'team_id': self.team['id'], 'expand': 'user'})

    @task(25)
    def list_memberships_for_team_expand_team(self):
        self.team = self._get_team()
        self._list_memberships({'team_id': self.team['id'], 'expand': 'team'})

    @task(25)
    def list_memberships_for_team_expand_user_and_team(self):
        self.team = self._get_team()
        self._list_memberships({'team_id': self.team['id'], 'expand': 'user,team'})

    # Get membership details
    @task(5)
    def membership_details(self):
        self._membership_details()

    @task(5)
    def membership_details_expand_user(self):
        self._membership_details({'expand': 'user'})

    @task(5)
    def membership_details_expand_team(self):
        self._membership_details({'expand': 'team'})

    @task(5)
    def membership_details_expand_user_and_team(self):
        self._membership_details({'expand': 'user,team'})

    # Delete membership
    @task(5)
    def delete_membership(self):
        self._delete_membership()

    # Disconnect
    @task(1)
    def stop(self):
        self._stop()


class TeamLocust(HttpLocust):
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'TeamAPITasks')]

    """
    Wait times were chosen using this formula to find an average, then +/- 20%
    desired requests per sec = (number of users) * 1000 / (average wait in ms)

    The assumed values are 15 rps = 100 * 1000 / 6667.
    If more or less than 100 users are desired, scale the wait time by the same
    factor to hold the rps steady, or choose a different factor if changing rps

    These numbers were chosen to be roughly double the daytime throughput of
    Forums (450 rpm = 7.5 rps), as reported on New Relic for prod-edx-forum.
    """

    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 5333))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 8000))
