"""
Load test for the Team API.
"""
from locust import task, HttpLocust
import os
import random
import requests
import string
import sys
from urlparse import urlparse

# Ignore SSL warnings for these tests.
requests.packages.urllib3.disable_warnings()

# Workaround for Locust running locustfiles as scripts instead of real
# packages.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lms'))
from lms import EdxAppTasks


STUDIO_HOST = os.getenv('STUDIO_HOST', 'http://localhost:8001')

TEAMS_CREATED = False

class BaseTeamsTask(EdxAppTasks):
    """
    Tasks for testing the Team API.
    """

    API_URL = '/api/team/v0'
    TOPICS_COUNT = 10
    TOPIC_NAME_LEN = 10
    TOPIC_DESCRIPTION_LEN = 10

    def __init__(self, *args, **kwargs):
        super(BaseTeamsTask, self).__init__(*args, **kwargs)
        self.teams = []

    def on_start(self):
        """Authenticate into Studio and create topics for the course, then log
        into LMS.
        """
        self.auto_auth(hostname=STUDIO_HOST, params={'staff': 'true'}, verify_ssl=False)  # log into Studio
        self.topics = [
            {
                'id': 'topic{}'.format(i),
                'name': 'Topic {}'.format(i),
                'description': 'Description for topic {}'.format(i)
            } for i in xrange(self.TOPICS_COUNT)
        ]
        global TEAMS_CREATED
        if not TEAMS_CREATED:
            TEAMS_CREATED = True
            self._create_topics()
        self.auto_auth(params={'staff': 'true'}, verify_ssl=False)  # log into LMS

    def _get_csrftoken(self, domain):
        try:
            csrftoken = self.client.cookies.get('csrftoken', default='')
        except requests.cookies.CookieConflictError:
            csrftoken = self.client.cookies.get('csrftoken', default='', domain=domain)
        return csrftoken

    def _default_headers(self, overrides=None):
        """Return the headers used for most operations in the Team API load
        tests, with an optional dictionary of extra headers.
        """
        csrftoken = self._get_csrftoken(urlparse(self.locust.host).hostname)
        defaults = {
            'X-CSRFToken': csrftoken,
            'Referer': self.locust.host
        }
        return dict(defaults, **overrides or {})

    def _create_topics(self):
        """Add `num_topics` test topics to the course."""
        csrftoken = self._get_csrftoken(urlparse(STUDIO_HOST).hostname)
        self.client.post(
            '{studio_host}/settings/advanced/{course_id}'.format(
                studio_host=STUDIO_HOST,
                course_id=requests.compat.quote(self.course_id)
            ),
            json={
                'teams_configuration': {
                    'value': {
                        'max_team_size': sys.maxint,
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

    def _request(self, method, path, **kwargs):
        """Send a request to the Team API."""
        kwargs['headers'] = self._default_headers(kwargs.get('headers'))
        kwargs['verify'] = False
        return getattr(self.client, method)(self.API_URL + path, **kwargs)

    def _get_team(self):
        """Get a randomly chosen team, creating one if it does not exist."""
        if self.teams == []:
            self._create_team()
        return random.choice(self.teams)

    def _create_team(self):
        """Create a team for this course. The topic which the team is
        associated with is randomly chosen from this course's topics, and the
        name and description are randomly generated. All optional parameters
        are left off.
        """
        json = {
            'course_id': self.course_id,
            'topic_id': random.choice(self.topics)['id'],
            'name': ''.join(random.sample(string.lowercase, self.TOPIC_NAME_LEN)),
            'description': ''.join(random.sample(string.lowercase, self.TOPIC_DESCRIPTION_LEN))
        }
        response = self._request('post', '/teams/', json=json)
        self.teams.append(dict(json, **{'id': response.json()['id']}))

    def _list_teams(self):
        """Retrieve the list of teams for a course."""
        url = '/teams/'
        self._request('get', url, params={'course_id': self.course_id}, name='/teams/?course_id=[id]')

    def _list_teams_for_topic(self):
        """Retrieve the list of teams for a course which are associated with a
        particular topic. The topic is randomly chosen from those associated
        with this course.
        """
        url = '/teams/'
        topic = random.choice(self.topics)['id']
        self._request(
            'get',
            url,
            params={'course_id': self.course_id, 'topic_id': topic},
            name='/teams/?course_id=[id]&topic_id=[id]'
        )

    def _team_detail(self):
        """Retrieve the detail view for a randomly chosen team."""
        team = self._get_team()
        self._request('get', '/teams/{}'.format(team['id']), name='/teams/[id]')

    def _update_team(self):
        """Update a randomly-chosen team for this course with a new
        description.
        """
        team = self._get_team()
        url = '/teams/{}'
        self._request(
            'patch',
            url.format(team['id']),
            name=url.format('[id]'),
            json={
                'description': ''.join(random.sample(string.lowercase, self.TOPIC_NAME_LEN))
            },
            headers={
                'content-type': 'application/merge-patch+json'
            }
        )

    def _list_topics(self):
        """Retrieve the list of topics for a course."""
        url = '/topics/'
        self._request('get', url, params={'course_id': self.course_id}, name='/topics/?course_id=[id]')

    def _topic_detail(self):
        """Retrieve the detail view for a randomly chosen topic."""
        topic = random.choice(self.topics)
        url = '/topics/{},{}'
        encoded_course_id = requests.compat.quote(self.course_id)
        self._request(
            'get',
            url.format(topic['id'], encoded_course_id),
            name=url.format('[topic_id]', '[course_id]')
        )

    def _stop(self):
        """Allow running as a nested or top-level task set."""
        if self.locust != self.parent:
            self.interrupt()


class TeamAPITasks(BaseTeamsTask):
    """Create and edit teams."""

    @task(5)
    def create_team(self):
        self._create_team()

    @task(2)
    def update_team(self):
        self._update_team()

    @task(1)
    def stop(self):
        self._stop()

    @task(5)
    def list_teams(self):
        self._list_teams()

    @task(2)
    def list_teams_for_topic(self):
        self._list_teams_for_topic()

    @task(8)
    def team_detail(self):
        self._team_detail()

    @task(5)
    def list_topics(self):
        self._list_topics()

    @task(8)
    def topic_detail(self):
        self._topic_detail()

    @task(1)
    def stop(self):
        self._stop()


class TeamLocust(HttpLocust):
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'TeamAPITasks')]
    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 7500))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 15000))
