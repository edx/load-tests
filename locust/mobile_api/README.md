Mobile API Locust Tests
============

This locust tests will be testing the following endpoints.

-/mobile_api.video_outlines.views:VideoSummaryList

-/mobile_api.users.views:UserCourseStatus

-/mobile_api.users.views:UserCourseEnrollmentsList

This test REQUIRES that auto auth is enabled in the test environment.
To enable auto auth, set the feature flag `AUTOMATIC_AUTH_FOR_TESTING` to True.


Usage
---------------

Start with:

`BASIC_AUTH_USER=user BASIC_AUTH_PASSWORD=pass locust --host="http://localhost:8000"`

Then visit `http://localhost:8089/`

Courses
---------------

In the constants.py file, there are many lists of courses. All courses were
sorted based on the number of blocks in the course. Split courses are not
entirely dependent on the number of blocks and have an ascending number of 
videos.

Specific values of the courses can be found at
https://openedx.atlassian.net/wiki/display/MA/Baseline

COURSE_ID_LIST_SMALL_A is a list of one lowest block count course

COURSE_ID_LIST_SMALL_B is a list of one highest block count course

COURSE_ID_LIST_MEDIUM_A is a list of 10 lowest block courses courses

COURSE_ID_LIST_MEDIUM_B is a list of 10 highest block courses courses

COURSE_ID_LIST_LARGE_A is a list of 20 lowest block courses courses

COURSE_ID_LIST_LARGE_B is a list of 20 highest block courses courses

COURSE_ID_LIST_XLARGE is a list of 40 highest block courses courses

SPLIT_COURSES_A is a list of 3 split courses. 
