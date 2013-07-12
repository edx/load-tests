'''
Helper file for seeding data (users, threads, comments)
into your database for testing purposes
'''

import json
from loremipsum import get_paragraphs, get_sentence
from helpers import CsApiCall

NUM_USERS = 1000
NUM_THREADS = 10000


class SeedUsersTransaction(CsApiCall):
    def __init__(self):
        super(SeedUsersTransaction, self).__init__()
        return

    def run(self, userid=1):

        timer_name = 'cs_put_user'
        method = 'put'

        url = '%s/users/%s' % (self.service_host, userid)
        data_or_params = {
            'username': u'test%s' % userid,
            'external_id': userid,
            'email': u'test%s@example.com' % userid,
            'api_key': self.api_key
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )
        return


class SeedThreadsTransaction(CsApiCall):
    def __init__(self):
        super(SeedThreadsTransaction, self).__init__()
        return

    def run(self, userid=1):

        timer_name = 'cs_post_thread'
        method = 'post'
        url = '%s/%s/threads' % (self.service_host, 'general')
        data_or_params = {
            'course_id': self.course_id,
            'api_key': self.api_key,
            'user_id': self.user_id,
            'body': get_paragraphs(3),
            'anonymous_to_peers': False,
            'title': get_sentence(),
            'commentable_id': u'general',
            'anonymous': False
        }
        response = self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        # Save the thread id to use in the mark as read transaction below
        thread_id = json.loads(response.content)['id']
        return thread_id


class SeedCommentsTransaction(CsApiCall):
    def __init__(self):
        super(SeedCommentsTransaction, self).__init__()
        return

    def run(self, thread_id):
        timer_name = 'cs_post_comment'
        method = 'post'
        url = '%s/threads/%s/comments' % (self.service_host, thread_id)
        data_or_params = {
            'body': get_paragraphs(3),
            'anonymous_to_peers': False,
            'user_id': self.user_id,
            'anonymous': False,
            'course_id': self.course_id,
            'api_key': self.api_key
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )


def main():
    # First clean your db with: `bundle exec rake db:clean`
    for x in xrange(1, NUM_USERS):
        SeedUsersTransaction().run(userid=x)
    for x in xrange(1, NUM_THREADS):
        thread_id = SeedThreadsTransaction().run()
        # create 1 comment for every 10 threads
        SeedCommentsTransaction().run(thread_id=thread_id)
        for y in xrange(1, 9):
            SeedThreadsTransaction().run()

    # Reindex with: `bundle exec rake db:reindex_search`
    return

if __name__ == '__main__':
    main()
