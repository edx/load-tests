from ecommerce_api_client import exceptions
from ecommerce_api_client.client import EcommerceApiClient
import requests
import slumber


class LocustResource(slumber.Resource):
    """Custom Slumber Resource which takes advantage of Locust's extended HttpSession."""
    def _request(self, method, data=None, files=None, params=None):
        serializer = self._store['serializer']
        url = self.url()

        headers = {'accept': serializer.get_content_type()}

        if not files:
            headers['content-type'] = serializer.get_content_type()
            if data is not None:
                data = serializer.dumps(data)

        # An optional argument that can be used to specify a label to use in Locust's statistics
        # instead of the actual URL. Can be used to group requests to the same API endpoint that vary
        # only by resource ID included in the URL into a single entry in Locust's statistics. For example,
        # requests to
        #   'http://localhost:8002/api/v2/baskets/1/order'
        # and
        #   'http://localhost:8002/api/v2/baskets/2/order'
        # might be grouped under the name:
        #   '/api/v2/baskets/:id/order/'
        # See: http://docs.locust.io/en/latest/api.html#httpsession-class/.
        name = params.pop('name', None)

        resp = self._store['session'].request(
            method,
            url,
            data=data,
            params=params,
            files=files,
            headers=headers,
            name=name
        )

        if 400 <= resp.status_code <= 499:
            exception_class = exceptions.HttpNotFoundError if resp.status_code == 404 else exceptions.HttpClientError
            raise exception_class('Client Error %s: %s' % (resp.status_code, url), response=resp, content=resp.content)
        elif 500 <= resp.status_code <= 599:
            raise exceptions.HttpServerError('Server Error %s: %s' % (resp.status_code, url), response=resp, content=resp.content)

        self._ = resp

        return resp


class LocustEcommerceApiClient(EcommerceApiClient):
    resource_class = LocustResource
