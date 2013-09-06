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
from time import sleep

# Number of users to create and enroll
NUM_USERS = 1
SUCCESS = 0
ERROR = 0

# Course ID to enroll users in
# Example: edx/999/2013_Spring

#COURSE_ID = "BerkeleyX/Stat2.3x/2013_SOND"         ## SPOC: 300
#COURSE_ID = "HahvahdX/BE101x/2013_Fall"            ## Small: 5k
#COURSE_ID = "8888/8888/importtesttest"             ## Small-average : 10k
#COURSE_ID = "Disney/1920/Mikis_Test_Course"        ## Large-average: 20k
#COURSE_ID = "YodaU/JEDI102/2013_Spring"            ## Large: 50k
#COURSE_ID = "StuckInThePast/Retro411/2013_Spring"  ## ENORMOUS: 100k

# Base email address to use
# e.g. success@simulator.amazonses.com
# We will use mailbox labelling to generate unique emails
# (for example, success+1234@simulator.amazonses.com
EMAIL_USERNAME = "success"
# others are: "suppressionlist", "bounce", "ooto", "complaint"
# see http://docs.aws.amazon.com/ses/latest/DeveloperGuide/mailbox-simulator.html
EMAIL_URL = "simulator.amazonses.com"

# Set a password for the users
USER_PASSWORD = "test"

# URL of the environment to test against
# Should not contain a trailing slash
TEST_URL = "https://edxapp.vpc-69f5a307.vpc.edx.org"


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

    resp = requests.get(TEST_URL + "/auto_auth", params=params, verify=False)

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
        cookies=cookies,
        verify=False
    )

    if resp.status_code != 200:
        print "Warning: Could not enroll user"
        return False

    return True


def create_and_enroll_user(no_op_mode):
    """
    Create users and enroll them in the course.

    If `no_op_mode` is True, print what we would have
    done instead of actually doing it.
    """
    global SUCCESS
    global ERROR

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
            if enroll_user(cookies):
                print "Enrolled {0} in {1} with email {2}".format(
                    username, COURSE_ID, full_email
                )
                SUCCESS += 1
            else:
                ERROR += 1
        else:
            ERROR += 1

if __name__ == "__main__":

    # Check if we're running in no-op mode
    NO_OP_MODE = False

    if len(sys.argv) > 1:
        if sys.argv[1] == '-n':
            NO_OP_MODE = True

        else:
            print "Usage: {0} [-n]\n   Use -n for no-op mode.".format(sys.argv[0])
            sys.exit(1)

    for user in range(NUM_USERS):
        if user % 10 == 0:
            print 'Users created: {0} ({1}% done)'.format(SUCCESS, (float(SUCCESS)/NUM_USERS)*100)
        create_and_enroll_user(NO_OP_MODE)
    print "Successfully enrolled {0} students ({1} failures)".format(SUCCESS, ERROR)
