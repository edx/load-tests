"""
Configurations shared across entrance exam tests.
"""

# Common URLS
LOGOUT_URL = u"/logout"
COURSE_URL_PREFIX = u"/courses/"

# Courses detail

COURSES = [
    {
        'course_type': 'Entrance Exam Uncleared',
        'course_id': u'course-v1:EE+EE1+EE2015',
        'exam_name': 'Entrance Exam',
        'coursware_link': '[EntranceExam Uncleared Courseware]',
        'exam_link': '[EntranceExam Uncleared Exam Page]',
        'input_choice': 'choice_brazil',
        'input_choice_type': 'incorrect'
    },
    {
        'course_type': 'Entrance Exam Cleared',
        'course_id': u'course-v1:EE2+EE2+EE2015',
        'exam_name': 'Entrance Exam',
        'coursware_link': '[EntranceExam Cleared Courseware]',
        'exam_link': '[EntranceExam Cleared Exam Page]',
        'input_choice': 'choice_indonesia',
        'input_choice_type': 'correct'
    },
    {
        'course_type': 'Simple Course',
        'course_id': u'course-v1:SE+SE1+SE2015',
        'exam_name': 'Simple Exam',
        'coursware_link': '[Simple Course Courseware]',
        'exam_link': '[Simple Exam Page]',
        'input_choice': 'choice_indonesia',
        'input_choice_type': 'correct'
    }
]

