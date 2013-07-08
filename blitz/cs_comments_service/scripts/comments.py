import os
from random import sample
from helpers import CsApiCall


class Comment(CsApiCall):
    """
    Comment API calls
    """
    def __init__(self, api_call='get_comment'):

        CsApiCall.__init__(self)

        if api_call == 'get_comment':
            self.comment_id = self._get_comment_id()
            self.method = 'get'
            self.url = '%s/comments/%s' % (self.service_host, self.comment_id)
            self.content = {
                'api_key': self.api_key,
                'recursive': False
            }

        return

    def _get_comment_id(self):
        # read in a list of possible threads to use
        this_dir = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(this_dir, '../data/comments.txt')
        with open(fname) as f:
            self.comments = f.readlines()

        # choose a random comment
        self.comment_id = sample(self.comments, 1)[0].rstrip('\n')
        return
