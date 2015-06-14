"""
Task helpers for the Bookmarks API.
"""
from lazy import lazy
import os
import random
import sys

from opaque_keys.edx.keys import CourseKey, UsageKey

# Work around the fact that Locust runs locustfiles as scripts within packages
# and therefore doesn't allow the use of absolute or explicit relative imports.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'helpers'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lms'))

from auto_auth_tasks import AutoAuthTasks
from lms import course_data

from api import BookmarksAPIMixin


class BookmarksTasksMixin(BookmarksAPIMixin):
    """ Task helpers for the Bookmarks API. """

    max_bookmarks = None  # Do not have more than this number of bookmarks for the course.

    @property
    def bookmarked_usage_ids(self):
        if not hasattr(self, '_bookmarked_usage_ids'):
            self._bookmarked_usage_ids = []
        return self._bookmarked_usage_ids

    def random_bookmarked_usage_id(self):
        """ Return the usage_id for a random bookmark. """
        if len(self.bookmarked_usage_ids) > 0:
            return random.choice(self.bookmarked_usage_ids)
        return None

    def get_course_bookmarks(self):
        """ GET bookmarks. """
        self.get_bookmarks(self.course_id)

    def create_a_bookmark(self):
        """ Create a bookmark. """
        if self.max_bookmarks and len(self.bookmarked_usage_ids) >= self.max_bookmarks:
            return

        usage_id = unicode(self.course_data.random_usage_key(self.course_key))
        for __ in range(9):
            if usage_id in self.bookmarked_usage_ids:
                usage_id = unicode(self.course_data.random_usage_key(self.course_key))
        response = self.create_bookmark(usage_id)
        if response.status_code == 201 and usage_id not in self.bookmarked_usage_ids:
            self.bookmarked_usage_ids.append(usage_id)

    def get_a_bookmark(self):
        """ Get a bookmark. """
        usage_id = self.random_bookmarked_usage_id()
        if usage_id:
            self.get_bookmark(usage_id)

    def delete_a_bookmark(self):
        """ Delete a bookmark. """
        usage_id = self.random_bookmarked_usage_id()
        if usage_id:
            response = self.delete_bookmark(usage_id)
            self.bookmarked_usage_ids.remove(usage_id)


class BookmarksTasksBase(AutoAuthTasks, BookmarksTasksMixin):
    """ Tasks for the Bookmarks API. """

    def on_start(self):
        """ Do authentication. """
        self.auto_auth(course_id=self.course_id)

    @lazy
    def course_id(self):
        """
        The complete id of the course we're configured to test with.
        """
        return os.getenv('COURSE_ID', 'edX/DemoX/Demo_Course')

    @lazy
    def course_data(self):
        """
        Accessor for the CourseData instance we're configured to test with.
        """
        course_data_name = os.getenv('COURSE_DATA', 'demo_course')
        return getattr(course_data, course_data_name)

    @lazy
    def course_key(self):
        """
        The course_id.
        """
        return CourseKey.from_string(self.course_id)
