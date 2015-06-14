"""
Load test for the edx-platform user API.

Usage:
  $ locust --host="http://localhost:8000"
"""
import os
from locust import HttpLocust

from tasks import BookmarksTasksBase


class BookmarksAPITasks(BookmarksTasksBase):
    """ Interaction with Bookmarks API """

    max_bookmarks = int(os.getenv('MAX_BOOKMARKS', 1000))

    tasks = {
        BookmarksTasksBase.get_course_bookmarks: int(os.getenv('BOOKMARKS_GET_LIST_WEIGHT', 10)),
        BookmarksTasksBase.create_a_bookmark: int(os.getenv('BOOKMARKS_CREATE_WEIGHT', 5)),
        BookmarksTasksBase.get_a_bookmark: int(os.getenv('BOOKMARKS_GET_WEIGHT', 1)),
        BookmarksTasksBase.delete_a_bookmark: int(os.getenv('BOOKMARKS_DELETE_WEIGHT', 1)),
    }


class BookmarksAPILocust(HttpLocust):
    task_set = BookmarksAPITasks
    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 8000))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 16000))
