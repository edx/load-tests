from helpers import CsApiCall
from loremipsum import get_sentence
from random import choice
from time import time
from json import loads

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

        start_timer = time()

        timer_name = 'cs_get_search_threads'
        method = 'get'
        url = '%s/search/threads' % (self.service_host)
        data_or_params = {
            'text': search_term,
            'course_id': self.course_id,
            'api_key': self.api_key,
            'user_id': self.user_id,
            'recursive': False,
            'sort_key': u'date',
            'sort_order': 'desc',
            'per_page': self.per_page,
            'page': 1
        }
        response = self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )
        num_pages = loads(response.content)['num_pages']

        latency = time() - start_timer

        # Report another timer grouped by number of results returned.
        # This can be use to correlate response time v. number of results.
        self.custom_timers['num_pages_%s' % num_pages] = latency

        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
