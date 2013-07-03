import json
from loremipsum import get_paragraphs, get_sentence
from helpers import CsApiCall
from time import time


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()
        return

    def run(self):
        # Capture the end to end time for the entire transaction
        start_e2e_timer = time()

        timer_name = 'CT_01_post_thread'
        method = 'post'
        url = '%s/%s/threads' % (self.service_host, '4x-edx-templates-course-Empty')
        data_or_params = {
            'course_id': self.course_id,
            'api_key': self.api_key,
            'user_id': self.user_id,
            'body': get_paragraphs(3),
            'anonymous_to_peers': False,
            'title': get_sentence(),
            'commentable_id': u'i4x-edx-templates-course-Empty',
            'anonymous': False
        }
        response = self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        # Save the thread id to use in the mark as read transaction below
        thread_id = json.loads(response.content)['id']

        self.get_user()
        self.get_user()

        timer_name = 'CT_02_get_threads'
        method = 'get'
        url = '%s/%s/threads' % (self.service_host, '4x-edx-templates-course-Empty')
        data_or_params = {
            'course_id': self.course_id,
            'api_key': self.api_key,
            'user_id': self.user_id,
            'recursive': False,
            'sort_key': u'date',
            'sort_order': 'desc',
            'per_page': self.per_page,
            'page': 1
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        self.get_user()
        self.get_user()

        timer_name = 'CT_03_mark_thread_read'
        method = 'get'
        url = '%s/threads/%s' % (self.service_host, thread_id)
        data_or_params = {
            'api_key': self.api_key,
            'user_id': self.user_id,
            'mark_as_read': True,
            'recursive': True
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        # Stop the timer and record the results
        e2e_latency = time() - start_e2e_timer

        # Record the transation timing results
        self.custom_timers['CT_00_create_thread_e2e'] = e2e_latency

        self.delay_for_pacing()
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
