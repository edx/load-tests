'''
Helper methods for API calls to the cs_comments_service
'''
import requests
from ConfigParser import ConfigParser
from random import randint
import os
from time import time, sleep


class CsApiCall(object):
    '''
    Object for multi-mechanize transactions
    '''
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
        self.pacing_delay = float(self.global_options['pacing_delay'])

        # Each iteration will use a random user
        self.user_id = randint(1, self.max_user_id)

        self.custom_timers = {}
        return

    def get_user(self):
        '''
        Call to the user that is used by every transaction
        by check_permissions_by_view
        '''

        method = 'get'
        url = '%s/users/%s' % (self.service_host, self.user_id)
        data_or_params = {
            'course_id': self.course_id,
            'api_key': self.api_key,
            'complete': True}
        response = self.perform_request(
            timer_name='check_permissions',
            method=method, url=url,
            data_or_params=data_or_params
        )
        return response

    def delay_for_pacing(self):
        '''
        Sleep for the pacing delay period in order to slow
        down the transactions to a reasonable volume
        '''
        sleep(self.pacing_delay)
        return


    def perform_request(self, method, url, data_or_params, timer_name):
        '''
        Do the request to the comment service.
        Wrapped in a timer to record the transaction timing.
        '''

        # Start the timer
        start_timer = time()

        # Make the request
        if method in ['post', 'put', 'patch']:
            response = requests.request(
                method, url, data=data_or_params, timeout=5
            )
        else:
            response = requests.request(
                method, url, params=data_or_params, timeout=5
            )

        # Verify that the transaction was successful
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code

        # Stop the timer. Do this after the assertion so that failed
        # transactions will not be included in the timing results.
        latency = time() - start_timer

        # Record the transation timing results
        self.custom_timers[timer_name] = latency

        return response
