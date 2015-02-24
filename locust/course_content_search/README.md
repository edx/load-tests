Course Content Search Locust Tests
============

This test REQUIRES that courseware search and indexing is enabled in the test environment.
To enable courseware search, set the feature flag `ENABLE_COURSEWARE_SEARCH` to True.
To enable courseware indexing, set the feature flag `ENABLE_COURSEWARE_INDEX` to True.


Usage
---------------

To start the test server on the host "www.example.com":

    >>> BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=password locust --host https://www.example.com

Then visit http://localhost:8089/

You can omit basic auth credentials if the test server is not protected by basic auth.

Other environment variables.

LMS_USER_EMAIL=email : (optional) You can provide an email to specify which user will log into the LMS during the test
                       (default) `honor@example.com`
LMS_USER_PASSWORD=pass : (optional) You can provide a password that will be used to authenticate the LMS user
                         (default) `edx`

Another example:

`BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=pass LMS_USER_EMAIL=email LMS_USER_PASSWORD=pass locust --host="http://benjilee.m.sandbox.edx.org"`


Courses
---------------

In the `constants.py` file, there is a list of course IDs named `COURSES`.
For now, there are only 3 course IDs in it.
Use that constant to provide a list of IDs for courses that will be used in the test.

There's also a dictionary named `SEARCH PHRASES`.
Modify the values of this dictionary to specify which phrases will be searched within a course during this test.
Dictionary keys are course IDs available in the `COURSES` constant.
Values include both phrases that can yield search results, as well as those phrases that would yield zero results.
