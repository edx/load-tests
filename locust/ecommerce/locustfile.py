""" Locust file for testing the ecommerce orders endpoint. """
import json
import os
import uuid
from locust import HttpLocust, TaskSet, task


# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])

EMAIL_USERNAME = "success"
EMAIL_URL = "simulator.amazonses.com"
# Set a password for the users
USER_PASSWORD = "test"


class ErrorResponse(Exception):

    """ The endpoint returned an error response. """

    pass


class AutoAuthTaskSet(TaskSet):
    """Use the auto-auth end-point to create test users. """

    def auto_auth(self):
        """Create a new account with given credentials and log in.

        This requires that the test server has the feature flag
        `AUTOMATIC_AUTH_FOR_TESTING` set to True.

        """
        del self.client.cookies["sessionid"]
        self.username = "{0}{1}".format(EMAIL_USERNAME, uuid.uuid4().hex[:20])
        self.full_email = "{0}@{1}".format(self.username, EMAIL_URL)
        params = {
            'password': USER_PASSWORD,
            'email': self.full_email,
            'username': self.username,
        }
        print "AUTO AUTHING"
        self.client.get("/auto_auth", params=params, verify=False, name="/auto_auth")
        return self.username


class PurchaseEndpointTasks(AutoAuthTaskSet):

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

    COURSE_ID = "edX/DemoX/Demo_Course"

    def on_start(self):
        """ Set up basic auth and check for the JWT secret key. """
        if BASIC_AUTH_CREDENTIALS is not None:
            self.client.auth = BASIC_AUTH_CREDENTIALS

        self.auto_auth()

    @property
    def _post_headers(self):
        """Headers for a POST request, including the CSRF token. """
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host
        }

    def _post(self, *args, **kwargs):
        """Make a POST request to the server.

        Skips SSL verification and sends the CSRF cookie.

        Raises a NotAuthorizedException if the server responds
        with a status 403.
        """
        kwargs['verify'] = False
        kwargs['headers'] = self._post_headers
        response = self.client.post(*args, **kwargs)
        return response

    @task(1)
    def purchase(self):
        """ Test the endpoint for purchasing specific courses. """
        data = {"course_id": self.COURSE_ID}
        resp = self._post('/commerce/orders/', data=json.dumps(data))
        if resp.status_code != 200:
            raise ErrorResponse


class WebsiteUser(HttpLocust):

    """ Run the PurchaseEndpointTasks. """

    task_set = PurchaseEndpointTasks
    min_wait = 5000
    max_wait = 9000
