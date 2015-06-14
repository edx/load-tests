"""
Helpers for the Bookmarks REST API.
"""
import os
import sys

# Work around the fact that this code doesn't live in a proper Python package.
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))
from request_helpers import RequestsMixin


class BookmarksAPIMixin(RequestsMixin):
    """ Helpers for the Bookmarks REST API. """

    def _bookmark_id_for_usage_id(self, usage_id):
        return u'{},{}'.format(self._username, usage_id)

    def get_bookmarks(self, course_id=None, page_size=50):
        """ GET list of bookmarks. """
        params = {
            'fields': 'display_name,path',
            'page_size': page_size,
        }
        if course_id:
            params['course_id'] = course_id,
        return self.make_get_request(
            u'/api/bookmarks/v1/bookmarks/', params=params,
            name='bookmarks:get_list'
        )

    def create_bookmark(self, usage_id):
        """ POST a new bookmark. """
        data = {'usage_id': usage_id}
        return self.make_post_request(
            u'/api/bookmarks/v1/bookmarks/', accept='json', data=data,
            name='bookmarks:create'
        )

    def get_bookmark(self, usage_id):
        """ GET a bookmark. """
        return self.make_get_request(
            u'/api/bookmarks/v1/bookmarks/{}/'.format(self._bookmark_id_for_usage_id(usage_id)), accept='json',
            name='bookmarks:get'
        )

    def delete_bookmark(self, usage_id):
        """ DELETE a bookmark. """
        return self.make_delete_request(
            u'/api/bookmarks/v1/bookmarks/{}/'.format(self._bookmark_id_for_usage_id(usage_id)), accept='json',
            name='bookmarks:delete'
        )
