"""
Configurations shared across proctoring tests.
"""

# Common URLS
ENROLLMENT_URL = u"/change_enrollment"
LOGOUT_URL = u"/logout"
COURSE_URL_PREFIX = u"/courses/"
START_EXAM_URL = u"/api/edx_proctoring/v1/proctored_exam/attempt"

# Course Ids and exam names

PROCTORED_COURSES = {
    u'course-v1:LTP+LTP1+2015': u"Load Test Proctored Exam 01",
    u'course-v1:LTP+LTP2+2015': u"Load Test Proctored Exam 02",
    u'course-v1:LTP+LTP3+2015': u"Load Test Proctored Exam 03"
}

NON_PROCTORED_COURSES = {
    u"course-v1:LTN+LTN1+2015": u"Load Test Non-Proctored Exam 01",
    u"course-v1:LTN+LTN2+2015": u"Load Test Non-Proctored Exam 02",
    u"course-v1:LTN+LTN3+2015": u"Load Test Non-Proctored Exam 03"
}
