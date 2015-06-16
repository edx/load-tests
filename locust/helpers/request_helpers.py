"""
Helpers for requests.
"""

class RequestsMixin(object):
    """ A mixin which simplifies making requests. """

    @property
    def post_headers(self):
        """ Return default headers for POST requests. """
        return {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host,
        }

    @property
    def delete_headers(self):
        """ Return default headers for DELETE requests. """
        return {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host,
        }

    def make_headers(self, method, accept=None, content_type=None, headers={}, **kwargs):
        """ Return headers for request. """
        request_headers = dict()
        request_headers.update(getattr(self, '{}_headers'.format(method), {}))

        if accept == 'json':
            request_headers['Accept'] = 'application/json, text/javascript, */*;'

        if content_type == 'json':
            request_headers['Content-type'] = 'application/json'

        request_headers.update(headers)
        return request_headers

    def make_request(self, method, path, accept=None, content_type=None, headers={}, *args, **kwargs):
        """ Make a request to the host. """
        kwargs['verify'] = False
        kwargs['headers'] = self.make_headers(method, accept, content_type, headers, **kwargs)
        return getattr(self.client, method)(path, *args, **kwargs)

    def make_get_request(self, path, *args, **kwargs):
        """ Make a GET request to the host. """
        return self.make_request('get', path, *args, **kwargs)

    def make_post_request(self, path, *args, **kwargs):
        """ Make a POST request to the host. """
        return self.make_request('post', path, *args, **kwargs)

    def make_delete_request(self, path, *args, **kwargs):
        """ Make a DELETE request to the host. """
        return self.make_request('delete', path, *args, **kwargs)
