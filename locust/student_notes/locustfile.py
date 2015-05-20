"""
These tests are meant to model the real ways in which a user interacts with the
student notes feature.  Currently there are three actions a learner can take in
student notes:

    - Create a note
    - Browse notes in the notes tab
    - Search notes in the notes tab

There are four TaskSets to model these actions.  Creating notes sends a direct
request from the client to the notes service.  Browsing and searching notes are
routed through the LMS, though we have an extra TaskSet for searching the notes
API directly to determine how much time is spent in the notes service vs in the
LMS.
"""
import json
from lazy import lazy
from locust import HttpLocust, task
import os
import random
import sys

# Work around the fact that Locust runs locustfiles as scripts within packages
# and therefore doesn't allow the use of absolute or explicit relative imports.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lms'))
from lms import EdxAppTasks

# NOTE: the host URL passed in via command-line '--host' flag is the host of
# the LMS!  Make sure to set the notes service URL via the NOTES_HOST
# environment variable.
NOTES_HOST = os.getenv('NOTES_HOST', 'http://localhost:8120')

# Constants used by the LMS when searching student notes.
HIGHLIGHT_TAG = "span"
HIGHLIGHT_CLASS = "note-highlight"


class BaseNotesMixin(object):
    """
    Base class for all TaskSet classes which interact with student notes.
    """
    data_directory = os.path.join(os.path.dirname(__file__), "data/")

    def on_start(self):
        """Code ran before any requests are made."""
        self.auto_auth()

    @lazy
    def text(self):
        """Return a large list of words."""
        with open(os.path.join(self.data_directory, 'basic_words.txt')) as f:
            return [word for line in f for word in line.split()]

    @property
    def annotator_auth_token(self):
        """Get the JWT key for making requests to the notes service from the LMS."""
        return self.client.get(
            '/courses/{course_id}/edxnotes/token/'.format(course_id=self.course_id),
            headers={'content-type': 'text/plain'}
        ).content

    def _request_from_notes_service(self, method, path, params_or_body, **kwargs):
        """
        Internal helper for making a request to the notes service.

        Arguments:
            method (str): HTTP method to execute.
            path (str): URL path to the resource being requested.
            params_or_body (dict): Dict of data to pass in the request.
        Returns:
            response: Response to the request that was made.
        """
        method = method.lower()
        kwargs.update({
            'headers': {
                'x-annotator-auth-token': self.annotator_auth_token,
                'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
                'content-type': 'application/json',
            }
        })
        params_or_body.update({
            "user": self._anonymous_user_id,
            "course_id": self.course_id,
        })
        if method == 'get':
            kwargs.update({'params': params_or_body})
        elif method in ['post', 'patch', 'put']:
            kwargs.update({'data': json.dumps(params_or_body)})
        return getattr(self.client, method)(NOTES_HOST + path, **kwargs)

    def get(self, path, params, **kwargs):
        """Internal helper for making a GET request to the notes service."""
        self._request_from_notes_service('get', path, params, **kwargs)

    def post(self, path, body, **kwargs):
        """Internal helper for making a POST request to the notes service."""
        self._request_from_notes_service('post', path, body, **kwargs)


class CreateNotesTasks(BaseNotesMixin, EdxAppTasks):
    """
    Create many sample student notes.  Because of the complex and unnecessary
    nature of scraping course text, both 'text' and 'quote' fields will be
    arbitrarily generated.
    """
    @task
    def post_note(self):
        """Post a note containing random text to the notes service."""
        endpoint = '/api/v1/annotations/'
        # Pass in the JWT token and CSRF token from edx platform
        data = {
            "text": ' '.join(pick_some(self.text, 25)),
            "quote": ' '.join(pick_some(self.text, 5)),
            "usage_id": "dummy_usage_id",
            "ranges": [
                {
                    "start": "/div[1]/p[1]",
                    "end": "/div[1]/p[1]",
                    "startOffset": 0,
                    "endOffset": 6
                }
            ],
        }
        self.post(endpoint, data)


class ListLmsNotesTasks(BaseNotesMixin, EdxAppTasks):
    """List notes on the LMS notes tab."""
    @task
    def list_notes(self):
        """List notes."""
        path = '/courses/{course_id}/edxnotes/'.format(course_id=self.course_id)
        self.client.get(path)


class SearchLmsNotesTasks(BaseNotesMixin, EdxAppTasks):
    """Search the notes API through the LMS, as a user would."""
    @task
    def search_notes(self):
        """Search notes for random text."""
        path = '/courses/{course_id}/edxnotes/search/'.format(course_id=self.course_id)
        params = {'text': ' '.join(pick_some(self.text, 4))}
        # Custom name ensures searches are grouped together in locust results.
        self.client.get(path, params=params, name=path + '?text=[search_text]')


class SearchNotesTasks(BaseNotesMixin, EdxAppTasks):
    """Search the notes API directly."""
    @task
    def search_notes(self):
        """Search notes for random text."""
        path = '/api/v1/search/'
        self.get(
            path,
            {
                'text': ' '.join(pick_some(self.text, 4)),
                'highlight': True,
                'highlight_tag': HIGHLIGHT_TAG,
                'highlight_class': HIGHLIGHT_CLASS
            },
            name=path + '?text=[search_text]'
        )


class NotesLocust(HttpLocust):
    # task_set = globals()[os.getenv('LOCUST_TASK_SET', 'CreateNotesTasks')]
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'SearchNotesTasks')]
    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 7500))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 15000))


def pick_some(sequence, num_items):
    """Return a list of up to `num_items` items from `sequence`."""
    return [random.choice(sequence) for _ in range(random.randint(1, num_items))]
