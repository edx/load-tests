from helpers import CsApiCall
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

        timer_name = __file__[:-3]
        method = 'get'
        url = '%s/users/%s/subscribed_threads' % (self.service_host, self.user_id)
        data_or_params = {
            'course_id': self.course_id,
            'api_key': self.api_key,
            'sort_key': choice(SORT_KEYS),
            'sort_order': 'desc',
            'per_page': 20,
            'page': 1
        }
        response = self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        self.delay_for_pacing()
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
