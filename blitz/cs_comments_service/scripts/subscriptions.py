from random import choice
from helpers import CsApiCall

SORT_KEYS = [
    'date',
    'activity',
    'votes',
    'comments'
]


class Subscription(CsApiCall):
    """
    User Subscriptions API calls
    """
    def __init__(self, api_call='get_user_subscribed_threads'):

        CsApiCall.__init__(self)

        if api_call == 'get_user_subscribed_threads':
            self.method = 'get'
            self.url = '%s/users/%s/subscribed_threads' % (self.service_host, self.user_id)
            self.content = {
                'course_id': self.course_id,
                'api_key': self.api_key,
                'sort_key': choice(SORT_KEYS),
                'sort_order': 'desc',
                'per_page': 20,
                'page': 1
            }

        # TODO: capture the data (content) of this transaction and code it up
        # elif api_call == 'post_user_subscriptions':
        #     self.method = 'post'
        #     self.url = '%s/users/%s/subscriptions' % (self.service_host, self.user_id)
        #     self.content = {
        #         'course_id': self.course_id,
        #         'api_key': self.api_key,
        #     }

        return
