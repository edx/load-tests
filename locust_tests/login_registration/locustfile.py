"""
Performance tests for the login and registration pages.

To start the test server on the host "www.example.com":

    >>> BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password locust --host https://www.example.com

To test the old login and registration pages, set the environment var `USE_OLD_PAGES=1`

Then visit http://localhost:8089/

You can omit basic auth credentials if the test server is not protected by basic auth.

"""

import os
import uuid
from locust import HttpLocust, TaskSet, task

# Basic auth
BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASSWORD'])

# Existing user in the LMS
LMS_USER_EMAIL = os.environ.get('LMS_USER_EMAIL', 'honor@example.com')
LMS_USER_PASSWORD = os.environ.get('LMS_USER_PASSWORD', 'edx')

# Use the old implementation of the login/registration pages
# This is useful for comparing old performance to the new implementation
USE_OLD_PAGES = os.environ.get('USE_OLD_PAGES', False)


class BasePage(object):
    """Base class for page objects. """

    def __init__(self, hostname, client):
        """Initialize the client.

        Arguments:
            hostname (unicode): The hostname of the test server, sent as the "Referer" HTTP header.
            client (Session): The test client used by locust.

        """
        self.hostname = hostname
        self.client = client

        if BASIC_AUTH_CREDENTIALS is not None:
            self.client.auth = BASIC_AUTH_CREDENTIALS

    def get(self, url):
        """HTTP GET request.

        Disables SSL verification, which may not be set up in the test environment.

        Arguments:
            url (unicode): The URL end-point used to make the request.

        Returns:
            Response

        """
        return self.client.get(url, verify=False)

    def post(self, url, params):
        """HTTP POST request.

        Includes CSRF token header and disables SSL verification.

        Arguments:
            url (unicode): The URL end-point used to make the request.
            params (dict): The POST params to send with the request.

        Returns:
            Response

        """
        return self.client.post(
            url,
            params,
            headers=self._post_headers,
            verify=False
        )

    @property
    def _post_headers(self):
        """Headers for a POST request, including the CSRF token. """
        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.hostname
        }


class OldLoginAndRegistrationPage(BasePage):
    """Interact with the old login and registration pages. """

    LOAD_URLS = {
        "login": "/login",
        "register": "/register",
        "reset_password": "/login",
    }

    def load(self, start):
        """Load a page.

        `start` must be either "login", "register", or "reset_password".
        """
        self.get(self.LOAD_URLS[start])

    def login(self, email, password, remember=False):
        """Log in using the old login page. """
        params = {
            "email": email,
            "password": password,
            "remember": "true" if remember else "false",
        }
        self.post("/login_ajax", params)

    def register(self, email, name, username, password):
        """Register a new account using the old registration page. """
        params = {
            "email": email,
            "name": name,
            "username": username,
            "password": password,
            "country": "US",
            "level_of_education": "",
            "gender": "",
            "year_of_birth": "",
            "mailing_address": "",
            "goals": "",
            "terms_of_service": "true",
            "honor_code": "true"
        }
        self.post("/create_account", params)

    def reset_password(self, email):
        """Request a password change using the old login page. """
        self.post("/password_reset/", {"email": email})


class LoginAndRegistrationPage(BasePage):
    """Interact with the combined login/registration page. """

    # The combined login registration page loads some of its content
    # using AJAX requests.  Simulate this by loading the base page,
    # then the form content.
    LOAD_URLS = {
        "login": ["/account/login/", "/user_api/v1/account/login_session/"],
        "register": ["/account/register/", "/user_api/v1/account/registration/"],
        "reset_password": ["/account/login/", "/user_api/v1/account/password_reset/"],
    }

    def load(self, start):
        """Load a page and simulate any initial AJAX requests.

        Arguments:
            start (unicode): Should be either "login", "register", or "reset_password"

        """
        for url in self.LOAD_URLS[start]:
            self.get(url)

    def login(self, email, password, remember=False):
        """Authenticate the user.

        Arguments:
            email (unicode): The user's email address.
            password (unicode): The user's password.
            remember (boolean): Whether "remember me" is checked.

        """
        params = {
            "email": email,
            "password": password,
            "remember": "true" if remember else "false",
        }
        self.post("/user_api/v1/account/login_session/", params)

    def register(self, email, name, username, password):
        """Register a new user account.

        Arguments:
            email (unicode): The user's email address.
            name (unicode): The user's full name.
            username (unicode): The username.
            password (unicode): The user's password.

        """
        params = {
            "email": email,
            "name": name,
            "username": username,
            "password": password,
            "level_of_education": '',
            "gender": '',
            "year_of_birth": '',
            "mailing_address": '',
            "goals": '',
            "country": "US",
            "honor_code": "true",
        }
        self.post("/user_api/v1/account/registration/", params)

    def reset_password(self, email):
        """Attempt to reset a user's password.

        This will trigger an email to the user account with an
        activation link.

        Arguments:
            email (unicode): The email address of the account to reset.

        """
        self.post("/account/password", {"email": email})


class UserBehavior(TaskSet):
    """User scripts that exercise the combined login/registration page. """

    def on_start(self):
        """Initialize the test. """
        page_class = OldLoginAndRegistrationPage if USE_OLD_PAGES else LoginAndRegistrationPage
        self.page = page_class(self.locust.host, self.client)

    @task
    def login_success(self):
        """Simulate a successful login. """
        self._reset_session()
        self.page.load("login")
        self.page.login(LMS_USER_EMAIL, LMS_USER_PASSWORD)

    @task
    def register_success(self):
        """Simulate a successful registration. """
        random_email = u"{user}@example.com".format(user=self._random_string())
        random_name = self._random_string()
        random_username = self._random_string()
        random_password = self._random_string()

        self._reset_session()
        self.page.load("register")
        self.page.register(random_email, random_name, random_username, random_password)

    @task
    def reset_password(self):
        """Reset a user's password. """
        self._reset_session()
        self.page.load("reset_password")
        self.page.reset_password(LMS_USER_EMAIL)

    def _reset_session(self):
        """Delete the session cookie to effectively log the user out. """
        del self.client.cookies["sessionid"]

    def _random_string(self):
        """Random string for emails, usernames, passwords, etc. """
        return uuid.uuid4().hex[:8]


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
