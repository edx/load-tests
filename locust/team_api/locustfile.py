"""
Load test for the Team API.
"""
from locust import task, HttpLocust, TaskSet
import os
import random
import string
import sys

# Workaround for Locust running locustfiles as scripts instead of real
# packages.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lms'))
from lms import EdxAppTasks


STUDIO_HOST = os.getenv('STUDIO_HOST', 'http://localhost:8001')

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
        """Create and authorize client before running tests."""
        self.auto_auth(params={'staff': 'true'})  # log into LMS
        self._create_topics(self.TOPICS_COUNT)
        self.client.post(  # log into Studio
            '{}/login_post'.format(STUDIO_HOST),
            {
                'email': self._email,
                'password': self._password
            },
            headers=self._default_headers()
        )

    def _default_headers(self, overrides=None):
        """Return the headers used for most operations in the Team API load
        tests, with an optional dictionary of extra headers.
        """
        defaults= {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host
        }
        return dict(defaults, **overrides or {})

    def _create_topics(self, num_topics):
        """Add `num_topics` test topics to the course."""
        self.topics = [
            {
                'id': 'topic{}'.format(i),
                'name': 'Topic {}'.format(i),
                'description': 'Description for topic {}'.format(i)
            } for i in xrange(num_topics)
        ]

        self.client.post(
            '{studio_host}/settings/advanced/{course_id}'.format(
                studio_host=STUDIO_HOST,
                course_id=self.course_id
            ),
            json={
                'teams_configuration': {
                    'value': {
                        'max_team_size': sys.maxint,
                        'topics': self.topics
                    }
                }
            },
            headers=self._default_headers({'Accept': 'application/json'})
        )

    def _request(self, method, path, **kwargs):
        """Send a request to the Team API."""
        default_headers = {
                'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
                'Referer': self.locust.host
            }
        kwargs['headers'] = self._default_headers(kwargs.get('headers'))

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
        data = {
            'course_id': self.course_id,
            'topic_id': random.choice(self.topics)['id'],
            'name': ''.join(random.sample(string.lowercase, self.TOPIC_NAME_LEN)),
            'description': ''.join(random.sample(string.lowercase, self.TOPIC_DESCRIPTION_LEN))
        }
        response = self._request('post', '/teams', data=data)
        self.teams.append(dict(data, **{'id': response.json()['id']}))

    def _list_teams(self):
        """Retrieve the list of teams for a course."""
        url = '/teams?course_id={}'
        self._request('get', url.format(self.course_id), name=url.format('[course_id]'))

    def _list_teams_for_topic(self):
        """Retrieve the list of teams for a course which are associated with a
        particular topic. The topic is randomly chosen from those associated
        with this course.
        """
        url = '/teams?course_id={}&topic_id={}'
        self._request(
            'get',
            url.format(self.course_id, random.choice(self.topics)['id']),
            name=url.format('[course_id]', '[topic_id]')
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
        url = '/topics/?course_id={}'
        self._request('get', url.format(self.course_id), name=url.format('[course_id]'))

    def _topic_detail(self):
        """Retrieve the detail view for a randomly chosen topic."""
        topic = random.choice(self.topics)
        url = '/topics/{},{}'
        self._request('get', url.format(topic['id'], self.course_id), name=url.format('[topic_id]', '[course_id]'))

    def _stop(self):
        """Allow running as a nested or top-level task set."""
        if self.locust != self.parent:
            self.interrupt()


class TeamAPITasks(BaseTeamsTask):
    """Create and edit teams."""

    @task(5)
    def create_team(self):
        self._create_team

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
