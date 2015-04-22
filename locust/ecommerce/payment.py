""" Locust tests for the E-Commerce Service payment notification endpoints. """
import base64
import hashlib
import hmac

from locust import task, TaskSet

from api import EcommerceApiClient
from config import (CYBERSOURCE_SECRET_KEY, ECOMMERCE_SERVICE_URL, ECOMMERCE_API_URL, ECOMMERCE_API_SIGNING_KEY,
                    LMS_USERNAME, LMS_EMAIL, SKU)


def sign(message, secret):
    """Compute a Base64-encoded HMAC-SHA256.

    Arguments:
        message (unicode): The value to be signed.
        secret (unicode): The secret key to use when signing the message.

    Returns:
        unicode: The message signature.
    """
    message = message.encode('utf-8')
    secret = secret.encode('utf-8')

    # Calculate a message hash (i.e., digest) using the provided secret key
    digest = hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()

    # Base64-encode the message hash
    signature = base64.b64encode(digest).decode()

    return signature


class PaymentTasks(TaskSet):
    def __init__(self, *args, **kwargs):
        super(PaymentTasks, self).__init__(*args, **kwargs)
        self.ecommerce_service_url = ECOMMERCE_SERVICE_URL
        self.cybersource_secret_key = CYBERSOURCE_SECRET_KEY
        self.api_client = EcommerceApiClient(ECOMMERCE_API_URL, ECOMMERCE_API_SIGNING_KEY, LMS_USERNAME, LMS_EMAIL,
                                             client=self.client)

    @task
    def cybersource_notification(self):
        """ Tests the CyberSource notification endpoint. """
        basket_id, amount = self._get_basket_details()
        data = self._get_cybersource_notification_data(basket_id, amount)

        url = '{}/payment/cybersource/notify/'.format(self.ecommerce_service_url)
        self.client.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def _generate_cybersource_signature(self, secret_key, data):
        """ Generate a signature for the given data dict. """
        keys = data[u'signed_field_names'].split(u',')

        message = u','.join([u'{key}={value}'.format(key=key, value=data[key]) for key in keys])
        return sign(message, secret_key)

    def _get_cybersource_notification_data(self, basket_id, amount):
        """ Returns a dict simulating a CyberSource payment response. """
        notification = {
            'decision': 'ACCEPT',
            'req_reference_number': basket_id,
            'transaction_id': '123456',
            'auth_amount': amount,
            'req_amount': amount,
            'req_tax_amount': '0.00',
            'req_currency': 'USD',
            'req_card_number': 'xxxxxxxxxxxx1111',
            'req_bill_to_forename': 'Ed',
            'req_bill_to_surname': 'Xavier',
            'req_bill_to_address_line1': '141 Portland Ave.',
            'req_bill_to_address_line2': '9th Floor',
            'req_bill_to_address_city': 'Cambridge',
            'req_bill_to_address_postal_code': '02141',
            'req_bill_to_address_state': 'MA',
            'req_bill_to_address_country': 'US'
        }

        notification['signed_field_names'] = ','.join(notification.keys())
        notification['signature'] = self._generate_cybersource_signature(self.cybersource_secret_key, notification)
        return notification

    def _get_basket_details(self):
        """ Creates a basket and returns its ID and amount. """
        basket = self.api_client.create_basket(SKU, True)
        return basket['id'], basket['payment_data']['payment_form_data']['amount']
