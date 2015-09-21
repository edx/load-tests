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

TEAMS_SETUP = False
TOPICS_COUNT = int(os.getenv('TOPICS_COUNT', 10))

class BaseTeamsTask(EdxAppTasks):
    """
    Tasks for testing the Team API.
    """

    API_URL = '/api/team/v0'
    TEAM_NAME_LEN = 10
    TEAM_DESCRIPTION_LEN = 10
    LOADED_TEAMS = 200
    MAX_TEAM_SIZE = 20
    # This is the number of teams we are going to prioritize for memberships so the users
    # are added to teams that are actually pulled back in the first few pages of results.
    # TOP_TEAM_SIZE * MAX_TEAM_SIZE should always be greater than the number of users being tested against
    # so that there are enough spots for all the users joining teams.
    TOP_TEAM_SIZE = 50

    top_name_teams = []
    teams = []
    topics = []
    user_memberships = {}
    team_member_counts = {}

    def on_start(self):
        """Authenticate into Studio and create topics for the course, then log
        into LMS.

        This assumes that you have already run a load test with team_init to set up the environment
        """
        self.auto_auth(params={'staff': 'true'}, verify_ssl=False)  # log into LMS

        global TEAMS_SETUP
        if not TEAMS_SETUP:
            # Ensure the setup is only run once
            TEAMS_SETUP = True
            self._load_topics()
            self._load_teams()
            self.top_name_teams[self.TOP_TEAM_SIZE:] = []

        self._enroll()

    def _load_teams(self):
        """ Load preexisting teams into memory via API call. """
        whitelist_keys = [
            'id',
            'course_id',
            'name',
            'description',
        ]

        # Calculate the number of pages to load.
        pages = self.LOADED_TEAMS / 10

        # We load teams page by page because requesting all teams at once is too slow.
        # Other spawned users start making requests against an empty teams list
        # before this can return and populate the teams if you try to grab
        # everything at once.
        for page in range(1, pages + 1):
            teams_response = self._list_teams({'page': page})
            results = teams_response.json()['results']

            if results != []:
                # only save the whitelisted keys which we are also saving when we create teams.
                blacklist_keys = set(results[0]) - set(whitelist_keys)
                for team in results:
                    for key in blacklist_keys:
                        del team[key]

                self.teams.extend(results)
                self.top_name_teams.extend(results)

    def _load_topics(self):
        """ Load preexisting topics into memory via API call. """
        topics_response = self._list_topics({'page_size': TOPICS_COUNT})
        topics = topics_response.json()['results']

        self.topics.extend(topics)

    def _enroll(self):
        """
        Enrolls the test's user in the course under test.
        """
        self.client.post(
            '/change_enrollment',
            data={'course_id': self.course_id, 'enrollment_action': 'enroll'},
            headers=self._default_headers(),
            name='enroll',
        )

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

    def _request(self, method, path, stub_run=False, **kwargs):
        """Send a request to the Team API."""
        kwargs['headers'] = self._default_headers(kwargs.get('headers'))
        kwargs['verify'] = False
        if stub_run:
            print '{} {}{}'.format(method, self.API_URL, path)
            print kwargs
            print '-----------'
        else:
            return getattr(self.client, method)(self.API_URL + path, **kwargs)

    def _append_to_top_name_teams(self, team):
        """ In place addition and resorting of top teams. """
        self.top_name_teams[self.TOP_TEAM_SIZE:] = [team]
        self.top_name_teams.sort(key=lambda t: t['name'])
        self.top_name_teams[self.TOP_TEAM_SIZE:] = []

    def _get_top_name_team(self):
        """ Randomly select a team from the top_name_teams list. """
        if self.top_name_teams == []:
            self._create_team()
        return random.choice(self.top_name_teams)

    def _get_team(self):
        """Get a randomly chosen team, creating one if it does not exist."""
        if self.teams == []:
            self._create_team()
        return random.choice(self.teams)

    def _get_search_query_string(self):
        """ Get a random word from a team name."""
        team = self._get_team()
        name_words = team['name'].split(' ')

        return random.sample(name_words, 1)

    def _create_team(self):
        """Create a team for this course. The topic which the team is
        associated with is randomly chosen from this course's topics. The
        randomly generated name is prefixed with the topic_id and course_id
        to produce varied search results when a piece of the name is chosen
        as the query string. The description is randomly generated. All
        optional parameters are left off.
        """
        topic_id = random.choice(self.topics)['id']

        json = {
            'course_id': self.course_id,
            'topic_id': topic_id,
            'name':  "{} {} {}".format(
                self.course_id,
                topic_id,
                ''.join(random.sample(string.lowercase, self.TEAM_NAME_LEN))
            ),
            'description': ''.join(random.sample(string.lowercase, self.TEAM_DESCRIPTION_LEN))
        }
        response = self._request('post', '/teams/', json=json)
        team = dict(json, **{'id': response.json()['id']})
        self.teams.append(team)
        self._append_to_top_name_teams(team)

    def _list_teams(self, params=None):
        """Retrieve the list of teams for a course."""
        url = '/teams/'
        default_params = {'course_id': self.course_id}
        return self._request('get', url, params=dict(default_params, **params or {}), name='/teams/?course_id=[id]')

    def _list_teams_for_topic(self, order_fields=None):
        """
        Retrieve the list of teams for a course which are associated with a
        particular topic. The topic is randomly chosen from those associated
        with this course, and the sort ordering is randomly selected from the available
        options.
        """
        url = '/teams/'
        if not order_fields:
            order_fields = ['name', 'last_activity_at', 'open_slots']
        topic = random.choice(self.topics)['id']
        order_by = random.choice(order_fields)
        self._request(
            'get',
            url,
            params={'course_id': self.course_id, 'topic_id': topic, 'order_by': order_by},
            name='/teams/?course_id=[id]&topic_id=[id]&order_by=[order]'
        )

    def _search_teams(self):
        """Retrieve the list of teams matching a particular query for a course.
        The query string is a randomly chosen word from the team name.
        """
        url = '/teams/'
        query_string = self._get_search_query_string()
        self._request(
            'get',
            url,
            params={'course_id': self.course_id, 'text_search': query_string},
            name='/teams/?course_id=[id]&text_search=[query_string]'
        )

    def _search_teams_for_topic(self):
        """Retrieve the list of teams matching a particular query for a course
        which are associated with a particular topic. The topic is randomly chosen
        from those associated with this course. The query string is a randomly
        chosen word from the team name.
        """
        url = '/teams/'
        topic = random.choice(self.topics)['id']
        query_string = self._get_search_query_string()
        self._request(
            'get',
            url,
            params={'course_id': self.course_id, 'topic_id': topic, 'text_search': query_string},
            name='/teams/?course_id=[id]&topic_id=[id]&text_search=[query_string]'
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
                'description': ''.join(random.sample(string.lowercase, self.TEAM_NAME_LEN))
            },
            headers={
                'content-type': 'application/merge-patch+json'
            }
        )

    def _list_topics(self, params=None):
        """
        Retrieve the list of topics for a course.
        The sort ordering is randomly selected from the available options.
        """
        url = '/topics/'

        default_params = {
            'course_id': self.course_id,
            'order_by': random.choice(['name', 'team_count'])
        }

        return self._request(
            'get', url, params=dict(default_params, **params or {}),
            name='/topics/?course_id=[id]&order_by=[order]'
        )

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

    def _create_membership(self, team_id):
        """
        Add a user to a team.

        This method assumes the following:
        *  self._username does not belong to any team
        *  The team represented by team_id is not full
        """
        url = '/team_membership/'

        json = {
            'team_id': team_id,
            'username': self._username
        }

        membership_created = True
        # If a user ends up joining a full team (due to a race condition)
        # we will catch the response and still mark it as a success since
        # that is the proper server response in that situation.
        with self._request('post', url, json=json, catch_response=True) as response:
            if response.status_code == 400 and "team is already full" in response.content:
                membership_created = False
                response.success()
            elif response.status_code != 200:
                membership_created = False

        if membership_created:
            self.user_memberships[self._username] = team_id
            count = self.team_member_counts.get(team_id, 0)
            count += 1
            self.team_member_counts[team_id] = count

    def _delete_membership(self):
        """
        Remove a user from a team.
        """
        team_id = self.user_memberships.get(self._username)

        if team_id:
            url = '/team_membership/{team_id},{username}'

            self._request(
                'delete',
                url.format(
                    team_id=team_id,
                    username=self._username
                ),
                name='/team_membership/[team_id],[username]'
            )

            self.user_memberships[self._username] = None

            count = self.team_member_counts.get(team_id, 0)
            count -= 1
            self.team_member_counts[team_id] = count

    def _change_membership(self):
        """
        Add the current user to a new team from the top_name_teams list.
        """
        # Will only delete if there is a membership to delete
        self._delete_membership()

        self.team = self._get_top_name_team()
        attempt = 0
        max_attempts = 25

        # Get a new team if it has reached the max size
        while(
            self.team_member_counts.get(self.team['id'], 0) >= self.MAX_TEAM_SIZE and
            attempt < max_attempts
        ):
            self.team = self._get_top_name_team()
            attempt += 1

        # create membership if we are still under the max retry limit
        if attempt < max_attempts:
            self._create_membership(self.team['id'])

    def _list_memberships_for_user(self):
        """
        Get the list of team memberships for the current user.
        """
        url = '/team_membership/'

        self._request(
            'get',
            url,
            params={'username': self._username},
            name='/team_membership/?username=[username]'
        )

    def _list_memberships_for_team(self):
        """
        Get the list of team memberships for a random team.
        """
        self.team = self._get_team()
        url = '/team_membership/'

        self._request(
            'get',
            url,
            params={'team_id': self.team['id']},
            name='/team_membership/?team_id=[id]'
        )

    def _stop(self):
        """Allow running as a nested or top-level task set."""
        if self.locust != self.parent:
            self.interrupt()
