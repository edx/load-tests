"""
Load test for setting up the Team API load test environment.

Usage:
  Create a new course in Studio.
  Set the environment variables based on what setup you want

  $ export COURSE_ID={new course id}
  $ export TOPICS_COUNT=20
  $ export TEAMS_COUNT=50000
  $ locust --host="http://localhost:8000"

  Run locust test with a single user to create topics and teams.

Supported Environment Variables:

  BASIC_AUTH_USER, BASIC_AUTH_PASS - if set, will use for HTTP Authentication
  LOCUST_TASK_SET - if set, will run the specified TaskSet (must be imported in this module)
  LOCUST_MIN_WAIT, LOCUST_MAX_WAIT - use to override defaults set in this module
  COURSE_ID - course that will be tested on the target host, default is set in lms.LmsTasks
  STUDIO_HOST - the URL where Studio is running, default set to http://localhost:8001.

  TOPICS_COUNT - Number of topics to create during setup *DEFAULT: 10*
  TEAMS_COUNT - Number of teams to create during setup (will be assigned randomly to topics) *DEFAULT: 1000*
"""
from locust import task, HttpLocust
import os
import sys
import requests
from urlparse import urlparse

# Workaround for Locust running locustfiles as scripts instead of real
# packages.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'team_api'))
from team_api import BaseTeamsTask

STUDIO_HOST = os.getenv('STUDIO_HOST', 'http://localhost:8001')
TEAMS_SETUP = False
TOPICS_COUNT = int(os.getenv('TOPICS_COUNT', 10))
TEAMS_COUNT = int(os.getenv('TEAMS_COUNT', 1000))


class TeamsInitTask(BaseTeamsTask):
    """
    Initializes the Team API data.
    """
    TOPICS_COUNT = 10

    def on_start(self):
        """Authenticate into Studio and create topics for the course, then log
        into LMS.
        """
        global TEAMS_SETUP
        if not TEAMS_SETUP:
            # Ensure the setup is only run once
            TEAMS_SETUP = True

            # log into Studio and create topics
            self.auto_auth(hostname=STUDIO_HOST, params={'staff': 'true'}, verify_ssl=False)
            self.topics = [
                {
                    'id': 'topic{}'.format(i),
                    'name': 'Topic {}'.format(i),
                    'description': 'Description for topic {}'.format(i)
                } for i in xrange(TOPICS_COUNT)
            ]
            self._create_topics()

            # log into LMS and create teams
            self.auto_auth(params={'staff': 'true'}, verify_ssl=False)
            for i in xrange(TEAMS_COUNT):
                self._create_team()

    def _create_topics(self):
        """Add test topics to the course based on number set by TOPICS_COUNT."""
        csrftoken = self._get_csrftoken(urlparse(STUDIO_HOST).hostname)
        self.client.post(
            '{studio_host}/settings/advanced/{course_id}'.format(
                studio_host=STUDIO_HOST,
                course_id=requests.compat.quote(self.course_id)
            ),
            json={
                'teams_configuration': {
                    'value': {
                        'max_team_size': self.MAX_TEAM_SIZE,
                        'topics': self.topics
                    }
                }
            },
            verify=False,
            headers={
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken,
                'Referer': STUDIO_HOST
            }
        )

    @task
    def noop(self):
        pass

class TeamLocust(HttpLocust):
    """ Set Locust variables. """
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'TeamsInitTask')]
    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 1000))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 2000))
