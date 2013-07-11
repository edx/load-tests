from helpers import CsApiCall
from time import time
from random import choice

class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()
        return

    def run(self):
        # Capture the end to end time for the entire transaction
        start_e2e_timer = time()

        timer_name = 'CT_01_post_thread'
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

        # Stop the timer and record the results
        e2e_latency = time() - start_e2e_timer

        # Record the transation timing results
        self.custom_timers['subscribe_thread_e2e'] = e2e_latency

        self.delay_for_pacing()
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
