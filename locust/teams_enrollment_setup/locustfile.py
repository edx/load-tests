"""
Simple run-once script to set up teams enrollment for a course that has students and other
real data, but no teams usage. Written as a locustfile to leverage previous work.

Usage:

  $ locust --host="http://localhost:8000"

  Be sure to run team_init first!

Supported Environment Variables:
    TEAM_ENROLLMENT_CSV - the file containing enrollment data
    COURSE_ID is important to have set, the default value fails
    All env vars used by team_init are used here as well
"""

from locust import task, HttpLocust
import os
import sys
import csv

# Workaround for Locust running locustfiles as scripts instead of real
# packages.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'team_api'))
from team_api import BaseTeamsTask

class TeamEnrollmentTask(BaseTeamsTask):
    """ The task, singular, that does the work of enrolling students """
    def on_start(self):
        self.user_list = []
        self._get_user_list()

        self.auto_auth(params={'staff': 'true'}, verify_ssl=False)  # log into LMS

        global TEAMS_SETUP
        if not TEAMS_SETUP:
            # Ensure the setup is only run once
            TEAMS_SETUP = True
            self._load_topics()
            self._load_teams()

        for user in user_list:
            #Note: we aren't checking if teams are full anywhere, so some users will not be on a team
            team_to_join = self._get_team()
            self._create_membership(username=user, team_id=team)

    def _get_user_list():
        with open(TEAMS_ENROLLMENT_CSV, 'r') as csv_input:
            reader = csv.DictReader(csv_input)
            for row in reader:
                self.user_list.extend(row['username'])

    def _create_membership(self, username, team_id):
        url = '/team_membership/'

        json = {
            'team_id': team_id,
            'username': username
        }

        # If a user ends up joining a full team
        # we will catch the response and still mark it as a success since
        # that is the proper server response in that situation.
        with self._request('post', url, json=json, catch_response=True) as response:
            if response.status_code == 400 and "team is already full" in response.content:
                response.success()

class TeamLocust(HttpLocust):
    """
    docstring goes here
    """
    task_set = globals()['TeamEnrollmentTask']

    #note: these wait values don't matter at all
    min_wait = 1000
    max_wait = 2000
