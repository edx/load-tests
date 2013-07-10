from helpers import CsApiCall
from random import randint


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()
        return

    def run(self):
        # Each iteration gets a random user's profile page
        self.profile_user = randint(1, self.max_user_id)

        timer_name = __file__[:-3]
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
        self.delay_for_pacing()
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
