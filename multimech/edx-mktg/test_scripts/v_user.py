"""
Simulate average user behavior on the marketing site.
"""

import numpy as np
import requests
import time

class Transaction(object):
    """
    Access marketing site pages using historical page access frequencies.
    """

    # Base URL of the marketing site
    BASE_URL = 'https://edx-loadtest.elasticbeanstalk.com'

    # Max number of URLs to hit in one transaction
    MAX_HITS = 5

    # List of marketing URLs accessed in the last 30 days
    MKTG_URLS = [
        '/course-list/allschools/allsubjects/allcourses',
        '/course-list/allschools/computer%20science/allcourses',
        '/course-list/allschools/allsubjects/new',
        '/course-list/allschools/engineering/allcourses',
        '/school/harvardx/allcourses',
        '/school/mitx/allcourses',
        '/',
        '/course-list/allschools/allsubjects/current',
        '/course-list/allschools/humanities/allcourses',
        '/course-list/allschools/math/allcourses',
        '/course-list/allschools/allsubjects/past',
        '/course-list/allschools/business%20and%20management/allcourses',
        '/course-list/allschools/economics%20and%20finance/allcourses',
        '/course-list/allschools/science/allcourses',
        '/course-list/allschools/physics/allcourses',
        '/course/harvard-university/cs50x/introduction-computer-science/1022',
        '/course-list/mitx/allsubjects/allcourses',
        '/course-list/allschools/statistics%20and%20data%20analysis/allcourses',
        '/course-list/allschools/social%20sciences/allcourses',
        '/course-list/harvardx/allsubjects/allcourses',
    ]

    # Probability of accessing each URL
    # (estimated from last 30 days)
    URL_PROBS = [
        0.64675,
        0.04875,
        0.04175,
        0.02675,
        0.02675,
        0.01975,
        0.01775,
        0.01575,
        0.01575,
        0.01475,
        0.01475,
        0.01375,
        0.01275,
        0.01275,
        0.01275,
        0.01175,
        0.01175,
        0.01175,
        0.01175,
        0.01175,
    ]

    def __init__(self):
        """
        Intialize custom timers.
        """
        self.custom_timers = dict()

    def run(self):
        """
        Access one or more URLs in the marketing site.
        """

        # Choose the number of hits
        num_hits = np.random.randint(1, self.MAX_HITS + 1)

        # Draw samples from the distribution over marketing URLs
        # The samples vector indicates the number of each
        # marketing URL to visit
        samples = np.random.multinomial(num_hits, self.URL_PROBS, size=1)
        samples = samples.reshape(len(self.URL_PROBS))

        # Retrieve the URLs
        url_list = []
        for index in range(samples.size):
            for num in range(samples[index]):
                url_list.append(self.MKTG_URLS[index])

        # Shuffle the URLs in-place
        np.random.shuffle(url_list)

        # Perform the requests
        for url in url_list:
            start = time.time()
            resp = requests.get(self.BASE_URL + url, verify=False)
            self.custom_timers['request_latency'] = time.time() - start
            assert(resp.status_code == 200)

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
