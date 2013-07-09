from helpers import CsApiCall


class User(CsApiCall):
    """
    User API calls
    """
    def __init__(self, api_call='get_user'):

        CsApiCall.__init__(self)

        if api_call == 'get_user':
            self.method = 'get'
            self.url = '%s/users/%s' % (self.service_host, self.user_id)
            self.params = {
                'course_id': self.course_id,
                'api_key': self.api_key,
                'complete': True
            }

        elif api_call == 'put_user':
            self.method = 'put'
            self.url = '%s/users/%s' % (self.service_host, self.user_id)
            self.params = {
                'username': u'roboto',
                'external_id': '2',
                'email': u'robot@edx.org'
            }

        elif api_call == 'get_user_active_threads':
            self.method = 'get'
            self.url = '%s/users/%s/active_threads' % (self.service_host, self.user_id)
            self.params = {
                'course_id': self.course_id,
                'api_key': self.api_key,
                'per_page': 20,
                'page': 1
            }

        return
