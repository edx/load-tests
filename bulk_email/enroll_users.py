"""
Script to create lots of users with Amazon SES test addresses
and enroll them in a course.

Assumes that we're testing against an environment with
auto_auth enabled and CSRF tokens disabled (load test settings).

1) Set the global variables below
2) `python enroll_users.py`

To run without actually submitting anything, pass the -n option:

    python enroll_users.py -n

This will print a description of what the script would have done.
"""
import sys
import uuid
import requests

# Number of users to create and enroll
NUM_USERS = 5

# Course ID to enroll users in
# Example: edx/999/2013_Spring
COURSE_ID = "edx/999/2013_Spring"

# Base email address to use
# e.g. success@simulator.amazonses.com
# We will use mailbox labelling to generate unique emails
# (for example, success+1234@simulator.amazonses.com
EMAIL_USERNAME = "success"
EMAIL_URL = "simulator.amazonses.com"

# Set a password for the users
USER_PASSWORD = "test"

# URL of the environment to test against
# Should not contain a trailing slash
TEST_URL = "http://dev.edx.org"


def auto_auth(username, email):
    """
    Use auto_auth end-point to login as a user.
    If the user doesn't exist, create it.

    Returns `(success, cookies)` tuple in which
    `success` indicates that we successfully logged in,
    and `cookies` is a dict of cookies set by the response.

    Since the cookies contain the session info,
    we can use them to enroll the user in the course.
    """
    params = {
        'password': USER_PASSWORD,
        'email': email,
        'name': username,
    }

    resp = requests.get(TEST_URL + "/auto_auth", params=params)

    if resp.status_code == 200:
        return (True, resp.cookies)

    elif resp.status_code == 403:
        print "Warning: Permission denied.  Please disable CSRF."
        return (False, None)

    else:
        print "Warning: Could not login as {0}; status code: {1}".format(username, resp.status_code)
        return (False, None)


def enroll_user(cookies):
    """
    Enroll a user in the course.
    We rely on the session being set correctly by auto_auth.
    """
    params = {
        'course_id': COURSE_ID,
        'enrollment_action': 'enroll',
    }

    resp = requests.post(
        TEST_URL + '/change_enrollment',
        data=params,
        cookies=cookies
    )

    if resp.status_code != 200:
        print "Warning: Could not enroll user"


def create_and_enroll_user(no_op_mode):
    """
    Create users and enroll them in the course.

    If `no_op_mode` is True, print what we would have
    done instead of actually doing it.
    """

    # Generate a random and hopefully unique email
    # Since we're using auto_auth, if this email isn't unique
    # the user will be retrieved instead of created,
    # so this won't cause an error (just possibly fewer
    # users than we expect).
    # The length limit is 255 on the LMS, so this should
    # be well under that (64 chars using "success@simulator.amazonses.com")
    username = "{0}+{1}".format(EMAIL_USERNAME, uuid.uuid4().hex)
    full_email = "{0}@{1}".format(username, EMAIL_URL)

    # If we're in no-op mode, just print what we would have done
    if no_op_mode:
        print "Enrolling {0} in {1} with email {2}".format(
            username, COURSE_ID, full_email
        )

    # Get or create the user using auto_auth
    # and enroll them in the course
    else:
        success, cookies = auto_auth(username, full_email)

        if success:
            enroll_user(cookies)


if __name__ == "__main__":

    # Check if we're running in no-op mode
    NO_OP_MODE = False

    if len(sys.argv) > 1:
        if sys.argv[1] == '-n':
            NO_OP_MODE = True

        else:
            print "Usage: {0} [-n]\n   Use -n for no-op mode.".format(sys.argv[0])
            sys.exit(1)

    for _ in range(NUM_USERS):
        create_and_enroll_user(NO_OP_MODE)
