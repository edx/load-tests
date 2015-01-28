"""
Constants for locustfile
"""
USER_PASSWORD = "test"
ENROLLMENT_API_BASE_URL = "/api/enrollment/v1"
MOBILE_API_BASE_URL = "/api/mobile/v0.5"
EMAIL_URL = "mobile.com"

COURSE_ID_LIST_SMALL_A = ["edX/DemoX/Demo_Course"]
COURSE_ID_LIST_SMALL_B = ["MITx/6.002_4x/3T2014"]
COURSE_ID_LIST_MEDIUM_A = [
    "edX/DemoX/Demo_Course",
    "BerkeleyX/ColWri2.3x/1T2014",
    "EPFLx/EE-102Bx/1T2014",
    "HarvardX/HSPH-HMS214x/2013_SOND",
    "BerkeleyX/ColWri2.1x/3T2013",
    "BerkeleyX/ColWri.2.2x/1T2015",
    "BerkeleyX/ColWri_2.1x/3T2014",
    "BerkeleyX/ColWri2.2x/1T2014",
    "UBCx/Forest222x/1T2015",
    "University_of_TorontoX/OEE101x/3T2013",
    ]
COURSE_ID_LIST_MEDIUM_B = [
    "ANUx/ANU-ASTRO2x/2T2014",
    "ANUx/ANU-ASTRO1x/1T2014",
    "WellesleyX/SOC108x/2014_SOND",
    "MITx/8.EFTx/3T2014",
    "BerkeleyX/GG101x-2/course",
    "UBCx/China300x/3T2014",
    "BerkeleyX/CS188x_1/1T2013",
    "MITx/3.091x_2/1T2014",
    "BerkeleyX/CS188.1x-4/1T2015",
    "MITx/6.002_4x/3T2014",
    'BerkeleyX/EECS149.1x/2T2014',
    'HarvardX/HDS1544.1x/2013_SOND',
    'CornellX/INFO2040x_Spring2015/1T2015',
    ]
COURSE_ID_LIST_LARGE_A = [
    "edX/DemoX/Demo_Course",
    "BerkeleyX/ColWri2.3x/1T2014",
    "EPFLx/EE-102Bx/1T2014",
    "HarvardX/HSPH-HMS214x/2013_SOND",
    "BerkeleyX/ColWri2.1x/3T2013",
    "BerkeleyX/ColWri.2.2x/1T2015",
    "BerkeleyX/ColWri_2.1x/3T2014",
    "BerkeleyX/ColWri2.2x/1T2014",
    "UBCx/Forest222x/1T2015",
    "University_of_TorontoX/OEE101x/3T2013",
    "HarvardX/1368.2x/2T2015",
    "UBCx/Water201x/3T2014",
    "University_of_TorontoX/D101x/1T2015",
    "IITBombayX/CS101.2x/3T2014",
    "IITBombayX/CS101.1x/2T2014",
    "HarvardX/PH525x/1T2014",
    "HarvardX/SW12x/2013_SOND"
    ]
COURSE_ID_LIST_LARGE_B = [
    "HarvardX/PH201x/2013_SOND",
    "KIx/KIexploRx/3T2014",
    "BerkeleyX/CS-191x/2013_August",
    "KIx/KIBEHMEDx/3T2014",
    "CornellX/HIST1514x_Fall2014/3T2014",
    "ANUx/ANU-ASTRO4x/1T2015",
    "CornellX/ENGRI1280x/1T2014",
    "HarvardX/PH210x/1T2014",
    "HarvardX/SW25x/1T2014",
    "ANUx/ANU-ASTRO3x/4T2014",
    "ANUx/ANU-ASTRO2x/2T2014",
    "ANUx/ANU-ASTRO1x/1T2014",
    "WellesleyX/SOC108x/2014_SOND",
    "MITx/8.EFTx/3T2014",
    "BerkeleyX/GG101x-2/course",
    "UBCx/China300x/3T2014",
    "BerkeleyX/CS188x_1/1T2013",
    "MITx/3.091x_2/1T2014",
    "BerkeleyX/CS188.1x-4/1T2015",
    "MITx/6.002_4x/3T2014"
    ]


COURSE_ID_LIST_XLARGE = [
    'edX/DemoX/Demo_Course',
    'BerkeleyX/ColWri2.3x/1T2014',
    'EPFLx/EE-102Bx/1T2014',
    'HarvardX/HSPH-HMS214x/2013_SOND',
    'BerkeleyX/ColWri2.1x/3T2013',
    'BerkeleyX/ColWri.2.2x/1T2015',
    'BerkeleyX/ColWri_2.1x/3T2014',
    'BerkeleyX/ColWri2.2x/1T2014',
    'UBCx/Forest222x/1T2015',
    'EPFLx/MF201x/1T2014',
    'University_of_TorontoX/OEE101x/3T2013',
    'HarvardX/1368.2x/2T2015',
    'UBCx/Water201x/3T2014',
    'HarvardX/HKS211.1x/3T2013',
    'HarvardX/1368.1x/3T2014',
    'EPFLx/BIO465.1x/4T2014',
    'IITBombayX/CS101.2x/3T2014',
    'IITBombayX/CS101.1x/2T2014',
    'HarvardX/PH525x/1T2014',
    'HarvardX/SW12x/2013_SOND',
    'BerkeleyX/EECS149.1x/2T2014',
    'HarvardX/PH201x/2013_SOND',
    'KIx/KIexploRx/3T2014',
    'BerkeleyX/CS-191x/2013_August',
    'KIx/KIBEHMEDx/3T2014',
    'CornellX/HIST1514x_Fall2014/3T2014',
    'ANUx/ANU-ASTRO4x/1T2015',
    'CornellX/ENGRI1280x/1T2014',
    'UWashingtonX/COMM220UWx/1T2014',
    'HarvardX/PH210x/1T2014',
    'HarvardX/SW25x/1T2014',
    'ANUx/ANU-ASTRO3x/4T2014',
    'ANUx/ANU-ASTRO2x/2T2014',
    'ANUx/ANU-ASTRO1x/1T2014',
    'WellesleyX/SOC108x/2014_SOND',
    'MITx/8.EFTx/3T2014',
    'UBCx/China300x/3T2014',
    'BerkeleyX/CS188x_1/1T2013',
    'MITx/3.091x_2/1T2014',
    'BerkeleyX/CS188.1x-4/1T2015',
    'MITx/6.002_4x/3T2014'
]

SPLIT_COURSES_A = [
    "course-v1:LinuxFoundationX+LFS101x.2+1T2015",
    "course-v1:BerkeleyX+GG101x-2+1T2015",
    "course-v1:MITx+6.00.2x_3+1T2015",
]

COURSE_ID_LIST = dict(
    SMALL_A=COURSE_ID_LIST_SMALL_A,
    SMALL_B=COURSE_ID_LIST_SMALL_B,
    MEDIUM_A=COURSE_ID_LIST_MEDIUM_A,
    MEDIUM_B=COURSE_ID_LIST_MEDIUM_B,
    LARGE_A=COURSE_ID_LIST_LARGE_A,
    LARGE_B=COURSE_ID_LIST_LARGE_B,
    XLARGE=COURSE_ID_LIST_XLARGE,
    SPLIT_A=SPLIT_COURSES_A
)
