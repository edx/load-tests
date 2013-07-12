from helpers import CsApiCall


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()
        return

    def run(self):
        self.get_user()

        timer_name = "cs_discussion_tab"
        method = 'get'
        url = '%s/threads' % (self.service_host)
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
        self.delay_for_pacing()
        return

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()
