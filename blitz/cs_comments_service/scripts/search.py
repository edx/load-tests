from random import choice
from loremipsum import get_sentence
from helpers import CsApiCall

SORT_KEYS = [
    'date',
    'activity',
    'votes',
    'comments'
]


class Search(CsApiCall):
    """
    Search API calls
    """
    def __init__(self, api_call='get_search_threads'):

        CsApiCall.__init__(self)

        if api_call == 'get_search_threads':
            # Search for a random word each time
            search_term = choice(get_sentence().split())

            self.method = 'get'
            self.url = '%s/search/threads' % (self.service_host)
            self.params = {
                'text': search_term,
                'course_id': self.course_id,
                'api_key': self.api_key,
                'user_id': self.user_id,
                'recursive': False,
                'sort_key': choice(SORT_KEYS),
                'sort_order': 'desc',
                'per_page': self.per_page,
                'page': 1
            }

        elif api_call == 'get_search_threads_commentable':
            # Search for a random word each time
            search_term = choice(get_sentence().split())

            # TODO parameterize the commentable id
            self.commentable_id = 'MReV_Summer2013_Skier'

            self.method = 'get'
            self.url = '%s/search/threads' % (self.service_host)
            self.params = {
                'text': search_term,
                'course_id': self.course_id,
                'api_key': self.api_key,
                'user_id': self.user_id,
                'recursive': False,
                'sort_key': choice(SORT_KEYS),
                'sort_order': 'desc',
                'per_page': self.per_page,
                'page': 1,
                'commentable_id': self.commentable_id
            }

        return
