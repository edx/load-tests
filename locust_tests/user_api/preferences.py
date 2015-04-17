"""
Locust tests for the preferences user API.
"""
import json
from time import sleep

from locustfile import UserAPITasks
from locust import task


class PreferencesTasks(UserAPITasks):

    @task(40)
    def get_preferences(self):
        """
        Gets account information for the user making the request. This will
        always return all the fields.
        """
        self.get(
            '/api/user/v0/preferences/{}'.format(self._username),
            name='user:preferences',
        )

    @task(5)
    def patch_multiple_preferences(self):
        """
        Updates the preference information for the user making the request.
        """
        patch_data = {
            UserAPITasks.generate_random_string(3): UserAPITasks.generate_random_string(30),
            self.preference_key: UserAPITasks.generate_random_string(10),
        }
        self.patch_preferences(self._username, patch_data)

    @task(40)
    def get_single_preference(self):
        """
        Return just a single preference for the user making the request (if the preference exists).
        """
        if self.preference_exists:
            self.get(
                '/api/user/v0/preferences/{}/{}'.format(self._username, self.preference_key),
                name='user:preferences_single',
            )

    @task(10)
    def put_single_preference(self):
        """
        Update a single preference for the user making the request.
        """
        self.put(
            '/api/user/v0/preferences/{}/{}'.format(self._username, self.preference_key),
            name='user:preferences_single',
            data=json.dumps(self.generate_random_string(10))
        )
        self.preference_exists = True

    @task(5)
    def delete_single_preference(self):
        """
        Delete a preference for the user making the request (assuming it exists).
        """
        if self.preference_exists:
            self.delete(
                '/api/user/v0/preferences/{}/{}'.format(self._username, self.preference_key),
                name='user:preferences_single',
            )
            self.preference_exists = False
