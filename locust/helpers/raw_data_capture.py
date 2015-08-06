"""
Code to capture all Locust request results in MongoDB.

To capture all your Locust request data, simply add these lines to your locustfile.py:

from raw_data_capture import RequestDatabaseLogger
db_evts = RequestDatabaseLogger()
db_evts.activate()

Optionally, add MongoDB connection information as so:

db_evts = RequestDatabaseLogger(mongo_host='localhost', mongo_port=27107)

If the import fails, you'll need to add a path to it before the import using something as below:

# Work around the fact that this code doesn't live in a proper Python package.
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))
"""

import os
import socket
import datetime
import pymongo
from locust import events as locust_events


class MongoConnection(object):
    """
    Base class for connecting to MongoDB.
    """
    def __init__(self, db, host, port=27017, tz_aware=True, user=None, password=None, **kwargs):
        """
        Create & open the connection - and authenticate.
        """
        self.database = pymongo.database.Database(
            pymongo.MongoClient(
                host=host,
                port=port,
                tz_aware=tz_aware,
                **kwargs
            ),
            db
        )

        if user is not None and password is not None:
            self.database.authenticate(user, password)


class RequestDatabaseLogger(object):
    """
    Class to log raw locust request data (both successes and failures) to MongoDB.
    Buffers the data and inserts it in batches to MongoDB.
    """
    # Flush request data events only after this many have been collected.
    EVENTS_BEFORE_FLUSH = 10

    # Enum of request outcomes.
    REQ_SUCCESS = 'success'
    REQ_FAILURE = 'failure'

    # MongoDB database info
    DB_NAME = 'locust_data'
    COLLECTION_NAME = 'requests'

    def __init__(self, mongo_host='localhost', mongo_port=27017):
        # Add list of request data.
        self._successes = []
        self._failures = []

        # Make a unique identifier for this Locust client.
        self.client_id = "{}:{}".format(socket.gethostname(), os.getpid())

        self.db = MongoConnection(db=self.DB_NAME, host=mongo_host, port=mongo_port)
        self.req_data = self.db.database[self.COLLECTION_NAME]

    def _apply_event(self, event_list, result, request_type, name, response_time, response_length, exception):
        event_data = {
            'result': result,
            'type': request_type,
            'name': name,
            'response_time': response_time,
            'response_length': response_length,
            'exception': exception,
            'client_id': self.client_id,
            'timestamp': datetime.datetime.utcnow()
        }
        event_list.append(event_data)

        # Check if list is big enough to insert.
        if len(event_list) >= self.EVENTS_BEFORE_FLUSH:
            self.req_data.insert(event_list)
            return True

        return False

    def success_handler(self, request_type, name, response_time, response_length, **kwargs):
        # Add to list.
        if self._apply_event(
            self._successes, self.REQ_SUCCESS,
            request_type, name, response_time, response_length, None
        ):
            # If events were inserted, clear the list.
            self._successes = []

    def failure_handler(self, request_type, name, response_time, exception, **kwargs):
        # Add to list.
        if self._apply_event(
            self._failures, self.REQ_FAILURE,
            request_type, name, response_time, None, unicode(exception)
        ):
            # If events were inserted, clear the list.
            self._failures = []

    def flush(self):
        """
        Flush all remaining events to the database.
        """
        if len(self._successes):
            self.req_data.insert(self._successes)
        if len(self._failures):
            self.req_data.insert(self._failures)
        self._successes = self._failures = []

    def activate(self):
        """
        Register all event handlers.
        """
        locust_events.request_success += self.success_handler
        locust_events.request_failure += self.failure_handler
        locust_events.quitting += self.flush


