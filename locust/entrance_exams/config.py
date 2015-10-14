"""
Configurations shared across entrance exam tests.
"""
import os

# Common URLS
LOGOUT_URL = u"/logout"
COURSE_URL_PREFIX = u"/courses/"

# Courses detail

COURSES = [
    {
        'course_id': u'course-v1:EE+EE1+EE2015',
        'exam_name': 'Entrance Exam',
        'coursware_link': '[EntranceExam Initial State Courseware]',
        'exam_link': '[EntranceExam Initial State Exam Page]',
        'input_choice': 'choice_brazil',
        'input_choice_type': 'incorrect'
    },
    {
        'course_id': u'course-v1:EE2+EE2+EE2015',
        'exam_name': 'Entrance Exam',
        'coursware_link': '[EntranceExam Passed Courseware]',
        'exam_link': '[EntranceExam Passed Exam Page]',
        'input_choice': 'choice_indonesia',
        'input_choice_type': 'correct'
    },
    {
        'course_id': u'course-v1:SE+SE1+SE2015',
        'exam_name': 'Simple Exam',
        'coursware_link': '[Simple Course Courseware]',
        'exam_link': '[Simple Exam Page]',
        'input_choice': 'choice_indonesia',
        'input_choice_type': 'correct'
    }
]

"""
Global variable for deciding which task should be run

TASK_TYPE=PreEntrance will run the Student Task for course with Entrance Exam without passing it
TASK_TYPE=PostEntrance will run the Student Task for course with Entrance Exam after it is passed
TASK_TYPE=Simple will run the Student Task for a simple course without Entrance Exam

Not using the TASK_TYPE will result in running the Instructor task
"""

TASK_TYPE = os.getenv('TASK_TYPE', '')
