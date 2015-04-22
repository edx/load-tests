""" Locust tests for the E-Commerce API. """
import json

import jwt

from locust import task, TaskSet
import requests

from config import ECOMMERCE_API_URL, ECOMMERCE_API_SIGNING_KEY, LMS_USERNAME, LMS_EMAIL, BASKET_ID


class EcommerceApiClient(object):
    """ E-Commerce API client. """

    def __init__(self, url, signing_key, username, user_email, client=None):
        self.url = url.strip('/')
        self.signing_key = signing_key
        self.username = username
        self.user_email = user_email

        self._client = client or requests.Session()
        self._client.headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'JWT {}'.format(self._get_jwt())
        })

    def _get_jwt(self):
        """
        Returns a JWT object with the specified user's info.

        Raises AttributeError if self.api_signing_key is not set.
        """
        data = {
            'username': self.username,
            'email': self.user_email
        }
        return jwt.encode(data, self.signing_key)

    def _create_api_url(self, path):
        """ Returns a complete URL to an API endpoint. """
        return self.url + path

    def list_payment_processors(self):
        """ Tests the /payment/processors/ endpoint. """
        url = self._create_api_url('/payment/processors/')
        return self._client.get(url).json()

    def retrieve_basket_order(self, basket_id):
        """ Retrieves the order associated with the specified basket. """
        url = self._create_api_url('/baskets/{}/order/'.format(basket_id))
        return self._client.get(url).json()

    def create_basket(self, sku, checkout=True):
        """ Creates a new basket with the specified product included. """
        url = self._create_api_url('/baskets/')
        data = {
            'products': [{'sku': sku}],
            'checkout': checkout,
            'payment_processor_name': 'cybersource'
        }
        response = self._client.post(url, data=json.dumps(data))
        return response.json()


class ApiTasks(TaskSet):
    def __init__(self, *args, **kwargs):
        super(ApiTasks, self).__init__(*args, **kwargs)
        self.api_client = EcommerceApiClient(ECOMMERCE_API_URL, ECOMMERCE_API_SIGNING_KEY, LMS_USERNAME, LMS_EMAIL,
                                             client=self.client)

    def _create_api_url(self, path):
        """ Returns a complete URL to an API endpoint. """
        return self.api_url + path

    @task
    def list_payment_processors(self):
        """ Tests the /payment/processors/ endpoint. """
        self.api_client.list_payment_processors()

    @task
    def retrieve_basket_order(self):
        """ Tests the /api/v2/baskets/:id/order/ endpoint. """
        self.api_client.retrieve_basket_order(BASKET_ID)
