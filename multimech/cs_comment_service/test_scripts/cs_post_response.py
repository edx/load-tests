import os
from random import sample
from loremipsum import get_paragraphs
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

        timer_name = 'PR_01_mark_thread_read'
        method = 'get'
        url = '%s/threads/%s' % (self.service_host, self.thread_id)
        data_or_params = {
            'mark_as_read': True,
            'api_key': self.api_key
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        timer_name = __file__[:-3]
        method = 'post'
        url = '%s/threads/%s/comments' % (self.service_host, self.thread_id)
        data_or_params = {
            'body': get_paragraphs(3),
            'anonymous_to_peers': False,
            'user_id': self.user_id,
            'anonymous': False,
            'course_id': self.course_id,
            'api_key': self.api_key
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
