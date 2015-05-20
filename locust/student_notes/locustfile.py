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
from contextlib import contextmanager
import json
from lazy import lazy
from locust import HttpLocust, task, TaskSet
import logging
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

NUM_NOTES = os.getenv('NUM_NOTES', 50)
NUM_WORDS = os.getenv('NUM_WORDS', 50)
NUM_TAGS = os.getenv('NUM_TAGS', 10)
NUM_SEARCH_TERMS = os.getenv('NUM_SEARCH_TERMS', 5)

# Constants used by the LMS when searching student notes.
HIGHLIGHT_TAG = "span"
HIGHLIGHT_CLASS = "note-highlight"

log = logging.getLogger(__name__)


class BaseNotesMixin(object):
    """
    Base class for all TaskSet classes which interact with student notes.
    """
    data_directory = os.path.join(os.path.dirname(__file__), "notes_data/")

    def __init__(self, *args, **kwargs):
        """Keep track of notes we post."""
        super(BaseNotesMixin, self).__init__(*args, **kwargs)
        self._notes = {}

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

    @contextmanager
    def get_posted_student_note(self, warning_message):
        """
        Yield a note that the current locust has created.  If there are none
        left, create a new note and yield it.
        """
        try:
            yield self._notes[random.choice(self._notes.keys())]
        except IndexError:  # No notes remaining
            log.debug(warning_message)
            yield self.post_note()

    def _request_from_notes_service(self, method, path, params_or_body=None, **kwargs):
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
        # Pass in the JWT token and CSRF token from edx platform
        kwargs.update({
            'headers': {
                'x-annotator-auth-token': self.annotator_auth_token,
                'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
                'content-type': 'application/json',
            }
        })
        if params_or_body is not None:
            if method == 'get':
                kwargs.update({'params': params_or_body})
            elif method in ['post', 'patch', 'put', 'delete']:
                kwargs.update({'data': json.dumps(params_or_body)})
        return getattr(self.client, method)(NOTES_HOST + path, **kwargs)

    def get(self, path, params=None, **kwargs):
        """Internal helper for making a GET request to the notes service."""
        return self._request_from_notes_service('get', path, params, **kwargs)

    def post(self, path, body=None, **kwargs):
        """Internal helper for making a POST request to the notes service."""
        return self._request_from_notes_service('post', path, body, **kwargs)

    def put(self, path, body=None, **kwargs):
        """Internal helper for making a PUT request to the notes service."""
        return self._request_from_notes_service('put', path, body, **kwargs)

    def delete(self, path, params=None, **kwargs):
        """Internal helper for making a DELETE request to the notes service."""
        return self._request_from_notes_service('delete', path, params, **kwargs)

    def post_note(self):
        """
        Post a note containing random text to the notes service.  Because of
        the complex and unnecessary nature of scraping course text, both 'text',
        'tags', and 'quote' fields will be arbitrarily generated.
        """
        data = {
            "user": self._anonymous_user_id,
            "course_id": self.course_id,
            "text": ' '.join(pick_some(self.text, NUM_WORDS)),
            "tags": ' '.join(pick_some(self.text, NUM_TAGS)),
            "quote": ' '.join(pick_some(self.text, 5)),
            "usage_id": 'i4x://edX/DemoX/html/030e35c4756a4ddc8d40b95fbbfff4d4',  # TODO remove this super-hacky solution by scraping usage ids and adding them to the CourseData dict
            "ranges": [
                {
                    "start": "/div[1]/p[1]",
                    "end": "/div[1]/p[1]",
                    "startOffset": 0,
                    "endOffset": 6
                }
            ],
        }
        note = json.loads(self.post('/api/v1/annotations/', data).content)
        self._notes[note['id']] = note
        return note

    def post_many_notes(self, num_notes):
        """Create many notes within the course for the current user."""
        for _ in xrange(num_notes):
            self.post_note()

    @property
    def is_child(self):
        """Return True if this TaskSet is a child of another TaskSet"""
        return isinstance(self.parent, TaskSet)


class ModifyNotesTasks(BaseNotesMixin, EdxAppTasks):
    """Create, edit, and delete notes with weighted probabilities."""
    @task(100)
    def create_note(self):
        """Create a note."""
        self.post_note()

    @task(20)
    def delete_note(self):
        """Delete a note."""
        collection_path = '/api/v1/annotations/'
        with self.get_posted_student_note('No notes left to delete.') as note:
            self.delete(collection_path + note['id'], note, name=collection_path + '[id]')
            self._notes.pop(note['id'])

    @task(33)
    def edit_note(self):
        """Edit a note."""
        collection_path = '/api/v1/annotations/'
        with self.get_posted_student_note('No notes left to edit.') as note:
            note['text'] = ' '.join(pick_some(self.text, NUM_WORDS))
            self.put(collection_path + note['id'], note, name=collection_path + '[id]')
            self._notes[note['id']] = note


class ListLmsNotesTasks(BaseNotesMixin, EdxAppTasks):
    """
    List notes on the LMS notes tab.
    """
    def on_start(self):
        super(ListLmsNotesTasks, self).on_start()
        self.post_many_notes(NUM_NOTES)

    @task(50)
    def list_notes(self):
        """List notes."""
        path = '/courses/{course_id}/edxnotes/'.format(course_id=self.course_id)
        self.client.get(path)

    @task(1)
    def stop(self):
        if self.is_child:
            self.interrupt()


class SearchLmsNotesTasks(BaseNotesMixin, EdxAppTasks):
    """
    Search the notes API through the LMS, as a user would.
    """
    def on_start(self):
        super(SearchLmsNotesTasks, self).on_start()
        self.post_many_notes(NUM_NOTES)

    @task(50)
    def search_notes(self):
        """Search notes for random text."""
        path = '/courses/{course_id}/edxnotes/search/'.format(course_id=self.course_id)
        params = {'text': ' '.join(pick_some(self.text, NUM_SEARCH_TERMS))}
        # Custom name ensures searches are grouped together in locust results.
        self.client.get(path, params=params, name=path + '?text=[search_text]')

    @task(1)
    def stop(self):
        if self.is_child:
            self.interrupt()


class BrowseLmsNotesTasks(TaskSet):
    """
    Parent TaskSet for viewing the notes list and searching the notes list.
    """
    tasks = {ListLmsNotesTasks: 3, SearchLmsNotesTasks: 2}


class SearchApiNotesTasks(BaseNotesMixin, EdxAppTasks):
    """Search the notes API directly."""
    @task
    def search_notes(self):
        """Search notes for random text."""
        path = '/api/v1/search/'
        self.get(
            path,
            {
                "user": self._anonymous_user_id,
                "course_id": self.course_id,
                'text': ' '.join(pick_some(self.text, NUM_SEARCH_TERMS)),
                'highlight': True,
                'highlight_tag': HIGHLIGHT_TAG,
                'highlight_class': HIGHLIGHT_CLASS
            },
            name=path + '?text=[search_text]'
        )


class NotesLocust(HttpLocust):
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'ModifyNotesTasks')]
    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 7500))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 15000))


def pick_some(sequence, num_items):
    """
    Return a list of between 1 and `num_items` (inclusive) items from
    `sequence`.
    """
    return random.sample(sequence, random.randint(1, num_items))
