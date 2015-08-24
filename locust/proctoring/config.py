"""
Configurations shared across proctoring tests.
"""

# Common URLS
ENROLLMENT_URL = u"/change_enrollment"
LOGOUT_URL = u"/logout"
COURSE_URL_PREFIX = u"/courses/"
START_EXAM_URL = u"/api/edx_proctoring/v1/proctored_exam/attempt"

# Course Ids
PROCTORED_COURSE_IDS = [
    u'course-v1:LTP+LTP1+2015',
    u'course-v1:LTP+LTP2+2015',
    u'course-v1:LTP+LTP3+2015',
    u'course-v1:LTP+LTP4+2015',
    u'course-v1:LTP+LTP5+2015'
]

# IDs of non proctored courses
NON_PROCTORED_COURSE_IDS = [
    u"course-v1:LTN+LTN1+2015",
    u"course-v1:LTN+LTN2+2015",
    u"course-v1:LTN+LTN3+2015",
    u"course-v1:LTN+LTN4+2015",
    u"course-v1:LTN+LTN5+2015"
]

# Exam names
PROCTORED_EXAM = u"Proctored Exam 01"

NON_PROCTORED_EXAM = u"Non Proctored Exam"
