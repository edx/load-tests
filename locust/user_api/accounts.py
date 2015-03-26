"""
Locust tests for the accounts user API.
"""
from locustfile import UserAPITasks
from locust import task


class AccountsTasks(UserAPITasks):

    def __init__(self, *args, **kwargs):
        """
        Add basic auth credentials to our client object when specified.
        """
        super(AccountsTasks, self).__init__(*args, **kwargs)
        # Create a couple "other" users.
        self.auto_auth()
        self.other_private_username = self._username
        self.populate_user_info(self.other_private_username, 'private')

        self.auto_auth()
        self.other_public_username = self._username
        self.populate_user_info(self.other_public_username, 'all_users')

    @task(10)
    def get_account_self(self):
        """
        Gets account information for the user making the request. This will
        always return all the fields.
        """
        self.get(
            '/api/user/v0/accounts/{}'.format(self._username), name='user:accounts_self',
        )

    @task(45)
    def get_account_other_private(self):
        """
        Gets the shared account information for a different user who marked profile information as private.
        """
        self.get(
            '/api/user/v0/accounts/{}'.format(self.other_private_username), name='user:accounts_private',
        )

    @task(40)
    def get_account_other_public(self):
        """
        Gets the shared account information for a different user who marked profile information as public.
        """
        self.get(
            '/api/user/v0/accounts/{}'.format(self.other_public_username), name='user:accounts_public',
        )

    @task(5)
    def patch_account_self(self):
        """
        Updates the account information for the user making the request. Updates bio, goals, and (full) name fields.
        """
        patch_data = {
            "name": UserAPITasks.generate_random_string(),
            "bio": UserAPITasks.generate_random_string(),
            "goals": UserAPITasks.generate_random_string()
        }
        self.patch_account(self._username, patch_data)
