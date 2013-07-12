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

        # Use a random sort key each time
        sort_key = choice(SORT_KEYS)

        self.get_user()

        timer_name = __file__[:-3]
        method = 'get'
        url = '%s/search/threads' % (self.service_host)
        data_or_params = {
            'text': search_term,
            'course_id': self.course_id,
            'api_key': self.api_key,
            'user_id': self.user_id,
            'recursive': False,
            'sort_key': sort_key,
            'sort_order': 'desc',
            'per_page': self.per_page,
            'page': 1
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        self.get_user()
        self.delay_for_pacing()
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
