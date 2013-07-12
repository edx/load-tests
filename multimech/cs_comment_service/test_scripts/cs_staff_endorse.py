import os
from random import sample
from helpers import CsApiCall


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()

        # read in a list of possible comments to use
        this_dir = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(this_dir, '../data/comments.txt')
        with open(fname) as f:
            self.comments = f.readlines()

        return

    def run(self):
        # choose a random comment to endorse
        self.comment_id = sample(self.comments, 1)[0].rstrip('\n')

        timer_name = "cs_staff_endorse"
        method = 'put'
        url = '%s/comments/%s' % (self.service_host, self.comment_id)
        data_or_params = {
            'endorsed': 'True',
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
