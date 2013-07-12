from helpers import CsApiCall
from loremipsum import get_sentence
from random import choice

SORT_KEYS = [
    'date',
    'activity',
    'votes',
    'comments'
]


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()
        return

    def run(self):
        # Search for a random word each time
        search_term = choice(get_sentence().split())

        # TODO parameterize the commentable id
        commentable_id = 'MReV_Summer2013_Skier'
        timer_name = "cs_get_search_threads_commentable"
        method = 'get'
        url = '%s/search/threads' % (self.service_host)
        data_or_params = {
            'text': search_term,
            'course_id': self.course_id,
            'api_key': self.api_key,
            'user_id': self.user_id,
            'recursive': False,
            'sort_key': choice(SORT_KEYS),
            'sort_order': 'desc',
            'per_page': self.per_page,
            'page': 1,
            'commentable_id': commentable_id
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
