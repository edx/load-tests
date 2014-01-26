JMeter tests
============
Load tests using JMeter.


LMS tests
---------

Required setup:

* Edx app (LMS and Studio) using `lms.envs.load_test` settings
* Set feature flags:

.. code :: bash

    FEATURES['AUTOMATIC_AUTH_FOR_LOAD_TESTING'] = True

* XQueue configured to point to grader stub
* Grader stub running in Heroku
* Manual Test Course installed via Studio import


Test assumptions:

* Uses relative frequencies of most common URLs.
* Assumes that all problem types are called with equal frequency.
* Sends all requests to one test course.
* Ramps up number of users (threads).
* Throttles throughput to approximately 1x current peak load in prod.


Marketing site tests
--------------------

Required setup:

* Drupal site
* To avoid crashing the server, make sure Varnish (caching) is turned on. Note that Varnish does not work with basic auth, so this must be turned off

Test assumptions:

* Distribution as follows (determined by Google Analytics):
** 35% to /
** 15% to /course-list/allschools/allsubjects/allcourses
** 50% equally distributed to the rest of the URLs (obtained using web crawler, see ../util/mktg_crawl.py)
* Ramps up number of users (threads)
* Throttles throughput at peak load in prod.
