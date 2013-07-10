import os
from random import sample
from helpers import CsApiCall


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()

        # read in a list of possible threads to use
        this_dir = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(this_dir, '../data/threads.txt')
        with open(fname) as f:
            self.threads = f.readlines()

        return

    def run(self):

        # choose a random thread to comment on
        self.thread_id = sample(self.threads, 1)[0].rstrip('\n')

        timer_name = __file__[:-3]
        method = 'delete'
        url = '%s/threads/%s/votes' % (self.service_host, self.thread_id)
        data_or_params = {
            'user_id': self.user_id,
            'api_key': self.api_key
        }
        self.perform_request(
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
