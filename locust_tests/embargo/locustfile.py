"""
Performance tests for IP-based and country-based embargos.

Currently, the new "country access" implementation of
the embargo middleware is hidden behind a feature flag.
You can enable the new implementation by setting:

    FEATURES['ENABLE_COUNTRY_ACCESS'] = True

You will also need to enable auto-auth:

    FEATURES['AUTOMATIC_AUTH_FOR_TESTING'] = True

You will then need to configure the embargo
rules in Django admin.  The relevant models are:

    * IPFilter: Configure global IP blacklists / whitelists.

    * RestrictedCourse: Configure course-specific access rules
        based on the user's country.  The user's country
        is inferred from the user's IP address and/or the user's
        profile.

To configure a country access rule, create a new RestrictedCourse
with a valid course ID.  Then add blacklist rules for the countries
you want to blacklist.

The worst-case scenario (in terms of number of database queries)
is when a user is attempting to access a restricted course and
the user is not blocked.  Testing this worst-case scenario is
therefore sufficient to upper-bound server-side latency.

To start the test server on the host "www.example.com":

    >>> BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password locust --host https://www.example.com

Then visit http://localhost:8089/

By default, the test uses the demo course (edX/DemoX/Demo_Course), but you
can override this by setting the `COURSE_ID_LIST` environment variable
to a list of slash-separated course keys.

The default nginx configuration in single-instance does NOT preserve
the incoming IP address (it sets it to 127.0.0.1).  To more accurately
simulate production, you need to change the nginx configuration
(in /edx/app/nginx/sites-available/lms):

    proxy_set_header X-Forwarded-Port $server_port;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header Host $http_host;

Then restart nginx with:

    $  sudo /etc/init.d/nginx restart

You can verify this change worked by setting the IPFilter blacklist
to include your IP address (use Django admin).  This should block
access to every page on the site.

To show whether the pages being accessed are blocked or not,
set the log level to "debug" using an environment variable:

    $ export LOG_LEVEL="DEBUG"

"""
import os
import logging
import random
from locust import HttpLocust, TaskSet, task

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])

COURSE_ID_LIST = os.environ.get('COURSE_ID_LIST', 'edX/DemoX/Demo_Course').split(",")


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))


class UserBehavior(TaskSet):
    """User scripts for testing country access embargos. """

    REQUESTS_PER_USER_ACCOUNT = 100

    def on_start(self):
        """Choose a course and authenticate. """
        if BASIC_AUTH_CREDENTIALS is not None:
            self.client.auth = BASIC_AUTH_CREDENTIALS
        self.course_id = random.choice(COURSE_ID_LIST)
        self._reset()

    @task
    def access_restricted_course(self):
        """Load a restricted page from the course. """
        # To test caching of user profile information, switch
        # to a new user account after a certain number of requests.
        if self.request_count > self.REQUESTS_PER_USER_ACCOUNT:
            self._reset()
        else:
            url = self._courseware_url()
            response = self.client.get(url, verify=False)
            self.request_count += 1
            if response.status_code == 403:
                self._reset()
            elif 'embargo' in response.url:
                LOGGER.debug(u"Blocked page: {url}".format(url=response.url))
            else:
                LOGGER.debug(u"Accessed page: {url}".format(url=response.url))


    def _reset(self):
        """Log in as a new user. """
        self.request_count = 0
        self._auto_auth()

    def _auto_auth(self):
        """Create a new account and enroll in the course.

        This requires that the test server has the feature flag
        `AUTOMATIC_AUTH_FOR_TESTING` set to True.

        """
        del self.client.cookies["sessionid"]
        params = {
            'course_id': self.course_id
        }
        self.client.get("/auto_auth", params=params, verify=False, name="/auto_auth")

    def _courseware_url(self):
        """Return a URL in the courseware.

        We test courseware URLs because country access settings
        apply to courseware, not to the rest of the site.
        """
        return u"/courses/{course_id}/info".format(course_id=self.course_id)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1
    max_wait = 5
