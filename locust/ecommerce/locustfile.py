""" Locust file for testing the ecommerce orders endpoint. """
import json
import os
import jwt
from locust import HttpLocust, TaskSet, task


# get the secret from environment variables
# Note: the JWT_SECRET must be set for this file to run correctly.
JWT_SECRET = os.environ['JWT_SECRET']

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])


class ErrorResponse(Exception):

    """ The endpoint returned an error response. """

    pass


class PurchaseEndpointTasks(TaskSet):

    """ Load tests for the purchase endpont.

    Notes for running this test:
        The expectation of the ecommerce endpoint is that users will be created
        from this token if they do not already exist. There are two methods you can
        use to keep your results consistent.

        Method 1: Clear out the DB of all new data between each run of the test.
        Method 2: Run the test once to generate a set of users in the DB.
                  Discard the results of this test. All tests after this should
                  be consistent because the users have all been created in the DB.

    """

    COURSE_SKU = "SEAT-HONOR-EDX-DEMOX-DEMO-COURSE"
    user_id = 1

    def on_start(self):
        """ Set up basic auth and check for the JWT secret key. """
        if BASIC_AUTH_CREDENTIALS is not None:
            self.client.auth = BASIC_AUTH_CREDENTIALS

    def _generate_user_token(self):
        """
        Return a JWT token for a unique user and user email combination.

        Args:
            None

        Returns:
            the JWT token that represents a unique username and email
        """
        user_base = 'edx'
        user = "{}-{}".format(user_base, self.user_id)
        user_email = "{}@example.com".format(user)
        token = jwt.encode({'username': user, 'email': user_email}, JWT_SECRET)

        self.user_id = self.user_id + 1
        return token

    @task(1)
    def purchase(self):
        """ Test the endpoint for purchasing specific courses. """
        data = {"sku": self.COURSE_SKU}
        headers = {
            'content-type': 'application/json',
            'Authorization': 'JWT ' + self._generate_user_token()
        }
        resp = self.client.post('/api/v1/orders/', data=json.dumps(data), headers=headers)
        if resp.status_code != 200:
            raise ErrorResponse


class WebsiteUser(HttpLocust):

    """ Run the PurchaseEndpointTasks. """

    task_set = PurchaseEndpointTasks
    min_wait = 5000
    max_wait = 9000
