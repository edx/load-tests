import os
from random import choice, sample
from loremipsum import get_paragraphs
from helpers import CsApiCall

SORT_KEYS = [
    'date',
    'activity',
    'votes',
    'comments'
]


class Thread(CsApiCall):
    """
    Thread API calls
    """
    def __init__(self, api_call='get_threads'):

        CsApiCall.__init__(self)

        if api_call == 'get_thread':
            self.thread_id = self._get_thread_id()
            self.method = 'get'
            self.url = '%s/threads/%s' % (self.service_host, self.thread_id)
            self.content = {
                'api_key': self.api_key,
                'user_id': self.user_id,
                'mark_as_read': True,
                'recursive': True
            }

        elif api_call == 'get_threads':
            self.method = 'get'
            self.url = '%s/threads' % (self.service_host)
            self.content = {
                'course_id': self.course_id,
                'api_key': self.api_key,
                'user_id': self.user_id,
                'recursive': False,
                'sort_key': choice(SORT_KEYS),
                'sort_order': 'desc',
                'per_page': self.per_page,
                'page': 1
            }

        elif api_call == 'post_thread_comment':
            self.thread_id = self._get_thread_id()
            self.method = 'post'
            self.url = '%s/threads/%s/comments' % (self.service_host, self.thread_id)
            self.content = {
                'body': get_paragraphs(3),
                'anonymous_to_peers': False,
                'user_id': self.user_id,
                'anonymous': False,
                'course_id': self.course_id,
                'api_key': self.api_key
            }

        return

    def _get_thread_id(self):
        # read in a list of possible threads to use
        this_dir = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(this_dir, '../data/threads.txt')
        with open(fname) as f:
            self.threads = f.readlines()

        # choose a random thread to comment on
        self.thread_id = sample(self.threads, 1)[0].rstrip('\n')
        return
