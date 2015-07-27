import os
import csv

"""
Configurations shared across certificate tasks.
"""

# Common URLS
LOGIN_URL = u"/login"
POST_CREDENTIALS_URL = u"/user_api/v1/account/login_session/"
ENROLLMENT_URL = u"/change_enrollment"
DASHBOARD_URL = u"/dashboard"
LOGOUT_URL = u"/logout"

# Correct choice for mcq
INPUT_CHOICE = u"choice_indonesia"

# Global Password
GLOBAL_STUDENT_PASSWORD = os.environ['GLOBAL_STUDENT_PASSWORD']

# IDs of self paced courses
SELF_PACED_COURSE_KEYS = [
    u"WebCertificate+SelfPaced01+2015",
    u"WebCertificate+SelfPaced02+2015",
    u"WebCertificate+SelfPaced03+2015",
    u"WebCertificate+SelfPaced04+2015",
    u"WebCertificate+SelfPaced05+2015"
    ]

# IDs of instructor paced courses
INSTRUCTOR_PACED_COURSE_KEYS = [
    u"WebCertificate+InstructorPaced01+2015",
    u"WebCertificate+InstructorPaced02+2015",
    u"WebCertificate+InstructorPaced03+2015",
    u"WebCertificate+InstructorPaced04+2015",
    u"WebCertificate+InstructorPaced05+2015",
    u"WebCertificate+InstructorPaced06+2015",
    u"WebCertificate+InstructorPaced07+2015",
    u"WebCertificate+InstructorPaced08+2015",
    u"WebCertificate+InstructorPaced09+2015",
    u"WebCertificate+InstructorPaced10+2015"
    ]

COURSE_URL_PREFIX = u"/courses/course-v1:"


def load_data_from_csv():
        """
        Open the csv file and read data from it
        :return: return the data as lists of lists
        """
        try:
            with open('credentials.csv', 'rb') as csv_file:
                csv_reader = csv.reader(csv_file)
                credentials_list = list(csv_reader)
            return credentials_list
        except IOError:
            return []

USER_CREDENTIALS = load_data_from_csv()
