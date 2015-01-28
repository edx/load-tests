"""
Sets up the users and their enrollments.
"""

import constants
import requests
import time

loadtest_url = "https://courses-loadtest.edx.org"

def auto_auth(user):
    """Create a new account with given credentials and log in.

    This requires that the test server has the feature flag
    `AUTOMATIC_AUTH_FOR_TESTING` set to True.

    """
    email = "{}@loadtest.com".format(user)
    params = {
        'password': constants.USER_PASSWORD,
        'email': email,
        'username': user,
        'staff': "true"
    }
    success = False
    url = "{}/auto_auth".format(loadtest_url)
    while not success:
        response = requests.get( url, params=params,)
        if not response.text.startswith("Logged"):
            print "Failed auto auth for {}".format(user)
            print "sleeping for 3 seconds before retrying"
            time.sleep(0)
        else:
            success = True
            print "successful auto auth for {}".format(user)
    del response.cookies["sessionid"]

while constants.LOADTEST_USERS:
    user = constants.LOADTEST_USERS.pop()
    time.sleep(0)
    auto_auth(user)

