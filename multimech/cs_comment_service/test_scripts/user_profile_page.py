from helpers import CsApiCall
from random import randint
from time import time


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()
        return

    def run(self):
        # Each iteration gets a random user's profile page
        self.profile_user = randint(1, self.max_user_id)

        # Capture the end to end time for the entire transaction
        start_e2e_timer = time()

        timer_name = 'UP_01_user_profile_page'
        method = 'get'
        url = '%s/users/%s/active_threads' % (self.service_host, self.profile_user)
        data_or_params = {
            'course_id': self.course_id,
            'api_key': self.api_key,
            'per_page': 20,
            'page': 1
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        self.get_user()
        self.get_user()

        # Stop the timer and record the results
        e2e_latency = time() - start_e2e_timer

        # Record the transation timing results
        self.custom_timers['UP_00_user_profile_e2e'] = e2e_latency

        self.delay_for_pacing()
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
