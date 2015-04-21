import random
import string
import logging
import json

from ..helpers.auto_auth_tasks import AutoAuthTasks


class UserAPITasks(AutoAuthTasks):
    """
    Base task class for accounts and preferences user APIs.
    """
    preference_key = "test_preference_key"
    preference_exists = False

    def _request(self, method, path, *args, **kwargs):
        """
        Single internal helper for setting up requests.
        """
        logging.debug(path)
        return getattr(self.client, method)(path, *args, **kwargs)

    def patch_account(self, username, patch_data, suffix=""):
        """ Update account info for given username. """
        self.patch(
            '/api/user/v0/accounts/{}'.format(username),
            data=json.dumps(patch_data),
            name='user:accounts'+suffix,
        )

    def patch_preferences(self, username, patch_data, suffix=""):
        """ Update preference info for given username. """
        self.patch(
            '/api/user/v0/preferences/{}'.format(username),
            data=json.dumps(patch_data),
            name='user:preferences'+suffix,
        )

    def patch(self, *args, **kwargs):
        """
        Perform a PATCH.
        """
        kwargs['headers'] = self.patch_headers
        return self._request('patch', *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Perform a GET.
        """
        return self._request('get', *args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Perform a PUT.
        """
        kwargs['headers'] = self.headers
        return self._request('put', *args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Perform a DELETE.
        """
        kwargs['headers'] = self.headers
        return self._request('delete', *args, **kwargs)

    @property
    def patch_headers(self):
        """
        Boilerplate headers for HTTP PATCH update requests.
        """
        return {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host,
            'content-type': 'application/merge-patch+json',
        }

    @property
    def headers(self):
        """
        Boilerplate headers for HTTP PUT and DELETE update requests.
        """
        return {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host,
            'content-type': 'application/json',
        }

    def on_start(self):
        """
        Setup code.
        """
        self.auto_auth()
        self.populate_user_info(self._username)

    def populate_user_info(self, username, privacy_setting=None):
        """
        Populate user with some account and preference data.
        """
        account_info = {
            "country": "US",
            "level_of_education": "m",
            "year_of_birth": 1980,
            "goals": UserAPITasks.generate_random_string(50),
            "mailing_address": UserAPITasks.generate_random_string(30),
            "bio": UserAPITasks.generate_random_string(200),
            "has_profile_image": bool(random.getrandbits(1))
        }
        self.patch_account(username, account_info, "_setup")

        if privacy_setting is None:
            # Randomly set privacy setting.
            is_private = bool(random.getrandbits(1))
            privacy_setting = "private" if is_private else "all_users"

        # Set a preference value for the user
        preference_info = {
            self.preference_key: UserAPITasks.generate_random_string(10),
            "account_privacy": privacy_setting
        }
        self.patch_preferences(username, preference_info, "_setup")
        self.preference_exists = True

    @staticmethod
    def generate_random_string(length=50):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
