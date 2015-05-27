import os
import logging
import sys

from locust import task, TaskSet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketingTasks(TaskSet):
    """Base task class for exercising marketing-related operations on the LMS."""

    def get(self, *args, **kwargs):
        """Perform a GET."""

        kwargs['headers'] = self.headers

        # Bypass SSL certificate verification
        kwargs['verify'] = False

        return self._request('get', *args, **kwargs)

    @property
    def headers(self):
        """Boilerplate headers for HTTP POST requests."""

        return {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def _request(
        self,
        method,
        path,
        *args,
        **kwargs
        ):
        """Single internal helper for setting up requests."""

        logger.debug(path)
        return getattr(self.client, method)(path, *args, **kwargs)


