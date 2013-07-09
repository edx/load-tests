"""
Helper methods for API calls to the cs_comments_service
"""
import os
from random import randint, sample
from ConfigParser import ConfigParser


class CsApiCall(object):
    """
    Object for cs_comments_service API calls
    """
    def __init__(self):

        # Read in the parameter values from the config file
        this_dir = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(this_dir, 'params.cfg')
        config = ConfigParser()
        config.read(fname)
        self.global_options = dict(config.items('global'))

        self.api_key = self.global_options['api_key']
        self.service_host = self.global_options['service_host']
        self.per_page = self.global_options['per_page']
        self.course_id = self.global_options['course_id']
        self.max_user_id = int(self.global_options['max_user_id'])

        # Each iteration will use a random user
        self.user_id = self._get_random_user()
        return

    def _get_random_user(self):
        # read in a list of possible user ids to use
        this_dir = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(this_dir, '../data/users.txt')
        with open(fname) as f:
            users = f.readlines()

        # choose a random user
        random_user = sample(users, 1)[0].rstrip('\n')
        return random_user.split(',')[0]
