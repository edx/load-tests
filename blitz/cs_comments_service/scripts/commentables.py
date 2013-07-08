from random import choice
from loremipsum import get_paragraphs, get_sentence
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
    def __init__(self, api_call='get_commentable_threads'):

        CsApiCall.__init__(self)

        if api_call == 'get_commentable_threads':
            # TODO parameterize the commentable id
            self.commentable_id = 'MReV_Summer2013_Skier'
            self.method = 'get'
            self.url = '%s/%s/threads' % (self.service_host, self.commentable_id)
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

        elif api_call == 'post_commentable_thread':
            # TODO parameterize the commentable id
            self.commentable_id = 'MReV_Summer2013_Skier'
            self.method = 'post'
            self.url = '%s/%s/threads' % (self.service_host, self.commentable_id)
            self.content = {
                'course_id': self.course_id,
                'api_key': self.api_key,
                'user_id': self.user_id,
                'body': get_paragraphs(3),
                'anonymous_to_peers': False,
                'title': get_sentence(),
                'commentable_id': self.commentable_id,
                'anonymous': False
            }

        return
