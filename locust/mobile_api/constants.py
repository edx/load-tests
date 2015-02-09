"""
Constants for locustfile
"""
USER_PASSWORD = "test"
ENROLLMENT_API_BASE_URL = "/api/enrollment/v1"
MOBILE_API_BASE_URL = "/api/mobile/v0.5"
EMAIL_URL = "mobile.com"

COURSE_ID_LIST_SMALL_A = ["edX/DemoX/Demo_Course"]
COURSE_ID_LIST_SMALL_B = ["MITx/EECS.6.002x/3T2013"]
COURSE_ID_LIST_SMALL_C = ["course-v1:MITx+6.002x_6x+1T2015"]
COURSE_ID_LIST_MEDIUM_A = [
    'edX/DemoX/Demo_Course',
    'BerkeleyX/ColWri2.3x/1T2014',
    'EPFLx/EE-102Bx/1T2014',
    'HarvardX/HSPH-HMS214x/2013_SOND',
    'BerkeleyX/ColWri2.1x/3T2013',
    'BerkeleyX/ColWri.2.2x/1T2015',
    'BerkeleyX/ColWri_2.1x/3T2014',
    'BerkeleyX/ColWri2.2x/1T2014',
    'UBCx/Forest222x/1T2015',
    'University_of_TorontoX/OEE101x/3T2013',
    'HarvardX/1368.2x/2T2015',
    ]
COURSE_ID_LIST_MEDIUM_B = [
    'HarvardX/PH210x/1T2014',
    'HarvardX/SW25x/1T2014',
    'ANUx/ANU-ASTRO3x/4T2014',
    'ANUx/ANU-ASTRO2x/2T2014',
    'ANUx/ANU-ASTRO1x/1T2014',
    'WellesleyX/SOC108x/2014_SOND',
    'UBCx/China300x/3T2014',
    'BerkeleyX/CS188x_1/1T2013',
    'MITx/3.091x_2/1T2014',
    'BerkeleyX/CS188.1x-4/1T2015',
    'MITx/EECS.6.002x/3T2013'
    ]
COURSE_ID_LIST_LARGE_A = [
    'edX/DemoX/Demo_Course',
    'BerkeleyX/ColWri2.3x/1T2014',
    'EPFLx/EE-102Bx/1T2014',
    'HarvardX/HSPH-HMS214x/2013_SOND',
    'BerkeleyX/ColWri2.1x/3T2013',
    'BerkeleyX/ColWri.2.2x/1T2015',
    'BerkeleyX/ColWri_2.1x/3T2014',
    'BerkeleyX/ColWri2.2x/1T2014',
    'UBCx/Forest222x/1T2015',
    'University_of_TorontoX/OEE101x/3T2013',
    'HarvardX/1368.2x/2T2015',
    'UBCx/Water201x/3T2014',
    'HarvardX/1368.1x/3T2014',
    'EPFLx/BIO465.1x/4T2014',
    'IITBombayX/CS101.2x/3T2014',
    'IITBombayX/CS101.1x/2T2014',
    'HarvardX/PH525x/1T2014',
    'HarvardX/SW12x/2013_SOND',
    'BerkeleyX/EECS149.1x/2T2014',
    'HarvardX/PH201x/2013_SOND',
    'KIx/KIexploRx/3T2014',
    ]
COURSE_ID_LIST_LARGE_B = [
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
    'HarvardX/PH210x/1T2014',
    'HarvardX/SW25x/1T2014',
    'ANUx/ANU-ASTRO3x/4T2014',
    'ANUx/ANU-ASTRO2x/2T2014',
    'ANUx/ANU-ASTRO1x/1T2014',
    'WellesleyX/SOC108x/2014_SOND',
    'UBCx/China300x/3T2014',
    'BerkeleyX/CS188x_1/1T2013',
    'MITx/3.091x_2/1T2014',
    'BerkeleyX/CS188.1x-4/1T2015',
    'MITx/EECS.6.002x/3T2013'
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
    'University_of_TorontoX/OEE101x/3T2013',
    'HarvardX/1368.2x/2T2015',
    'UBCx/Water201x/3T2014',
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
    'HarvardX/PH210x/1T2014',
    'HarvardX/SW25x/1T2014',
    'ANUx/ANU-ASTRO3x/4T2014',
    'ANUx/ANU-ASTRO2x/2T2014',
    'ANUx/ANU-ASTRO1x/1T2014',
    'WellesleyX/SOC108x/2014_SOND',
    'UBCx/China300x/3T2014',
    'BerkeleyX/CS188x_1/1T2013',
    'MITx/3.091x_2/1T2014',
    'BerkeleyX/CS188.1x-4/1T2015',
    'MITx/EECS.6.002x/3T2013'
]

SPLIT_COURSES_A = [
    "course-v1:LinuxFoundationX+LFS101x.2+1T2015",
    "course-v1:BerkeleyX+GG101x-2+1T2015",
    "course-v1:MITx+6.002x_6x+1T2015",
]

MIDDLE_VIDEO_LIST = {
'edX/DemoX/Demo_Course': 'i4x://edX/DemoX/video/5c90cffecd9b48b188cbfea176bf7fe9',
'BerkeleyX/ColWri2.3x/1T2014': 'i4x://BerkeleyX/ColWri2.3x/video/9eaafbb3d8bc4e33ba887f9647dffcd1',
'EPFLx/EE-102Bx/1T2014': 'i4x://EPFLx/EE-102Bx/video/ac2135293484443e9905186b6054cda0',
'HarvardX/HSPH-HMS214x/2013_SOND': 'i4x://HarvardX/HSPH-HMS214x/video/f708a1e5e73f4d4fadca570f87901fd9',
'BerkeleyX/ColWri2.1x/3T2013': 'i4x://BerkeleyX/ColWri2.1x/video/52740765719848b789270f99c0a70a3f',
'BerkeleyX/ColWri.2.2x/1T2015': 'i4x://BerkeleyX/ColWri.2.2x/video/4bbae2b993554faeb3f0cf7f3386f1d1',
'BerkeleyX/ColWri_2.1x/3T2014': 'i4x://BerkeleyX/ColWri_2.1x/video/308f592479c34bd8a566e781620d4daa',
'BerkeleyX/ColWri2.2x/1T2014': 'i4x://BerkeleyX/ColWri2.2x/video/4bbae2b993554faeb3f0cf7f3386f1d1',
'UBCx/Forest222x/1T2015': 'i4x://UBCx/Forest222x/video/d68e73513ce84e23aa90abbb842a8dbe',
'University_of_TorontoX/OEE101x/3T2013': 'i4x://University_of_TorontoX/OEE101x/video/60136e9a50c54ad0858edd421afbddd8',
'HarvardX/1368.2x/2T2015': 'i4x://HarvardX/1368.2x/video/389869ff56e549ef8a17ac34ec41c27b',
'UBCx/Water201x/3T2014': 'i4x://UBCx/Water201x/video/d36895a410f64c50b1ec390cff143336',
'HarvardX/1368.1x/3T2014': 'i4x://HarvardX/1368.1x/video/f13926bef1014d7ea620644216fea3f5',
'EPFLx/BIO465.1x/4T2014': 'i4x://EPFLx/BIO465.1x/video/bf381a6a14294e8bb83efa848fff9054',
'IITBombayX/CS101.2x/3T2014': 'i4x://IITBombayX/CS101.2x/video/bd0dc555311846289cd28b7242612e08',
'IITBombayX/CS101.1x/2T2014': 'i4x://IITBombayX/CS101.1x/video/ac88b4fd7d1c4dc4aab8a3a912d6029d',
'HarvardX/PH525x/1T2014': 'i4x://HarvardX/PH525x/video/c175ccea0b9d4d3e85c52afe24cd6e15',
'HarvardX/SW12x/2013_SOND': 'i4x://HarvardX/SW12x/video/f988d95fa8bf478da827210acf8d4d24',
'BerkeleyX/EECS149.1x/2T2014': 'i4x://BerkeleyX/EECS149.1x/video/040a31eba13141108c1ff96571fe2c91',
'HarvardX/PH201x/2013_SOND': 'i4x://HarvardX/PH201x/video/ffcbafde11114092ac0dfe0bc59078fe',
'KIx/KIexploRx/3T2014': 'i4x://KIx/KIexploRx/video/7749a7ac4c2342e88ee469505c8231ce',
'BerkeleyX/CS-191x/2013_August': 'i4x://BerkeleyX/CS-191x/video/a525c4be16174db2ae7cf0d902e606c9',
'KIx/KIBEHMEDx/3T2014': 'i4x://KIx/KIBEHMEDx/video/ab26d24e26574b9e90c7cf8ff29a60bf',
'CornellX/HIST1514x_Fall2014/3T2014': 'i4x://CornellX/HIST1514x_Fall2014/video/b972af946da3476fa66425ca922ef039',
'ANUx/ANU-ASTRO4x/1T2015': 'i4x://ANUx/ANU-ASTRO4x/video/bf79a890b6b548e6b41610fdce3e7946',
'CornellX/ENGRI1280x/1T2014': 'i4x://CornellX/ENGRI1280x/video/fd06a414b6844983bc801cb8236b8f13',
'HarvardX/PH210x/1T2014': 'i4x://HarvardX/PH210x/video/42a41ddb97d54531a8b1e02889c1b71d',
'HarvardX/SW25x/1T2014': 'i4x://HarvardX/SW25x/video/48d10ffb9a04445797c98356803b2f5a',
'ANUx/ANU-ASTRO3x/4T2014': 'i4x://ANUx/ANU-ASTRO3x/video/e97da4b4335b42afb00178cf0f3ff2c5',
'ANUx/ANU-ASTRO2x/2T2014': 'i4x://ANUx/ANU-ASTRO2x/video/e465f11b975b4026898528e8918d64ae',
'ANUx/ANU-ASTRO1x/1T2014': 'i4x://ANUx/ANU-ASTRO1x/video/7fec42890a5547d8afe593320dc06add',
'WellesleyX/SOC108x/2014_SOND': 'i4x://WellesleyX/SOC108x/video/f7dde3b0d5c44595bc46ea69be63e88c',
'UBCx/China300x/3T2014': 'i4x://UBCx/China300x/video/96c428d558de4ffd83243dcb2efca91c',
'BerkeleyX/CS188x_1/1T2013': 'i4x://BerkeleyX/CS188x_1/video/378e8f35daa044c8becfa1ace16045c1',
'MITx/3.091x_2/1T2014': 'i4x://MITx/3.091x_2/video/lecture_17b_7v2',
'BerkeleyX/CS188.1x-4/1T2015': 'i4x://BerkeleyX/CS188.1x-4/video/75de6e99177344e4a9c6e2d9b7b8579c',
'MITx/EECS.6.002x/3T2013': 'i4x://MITx/EECS.6.002x/video/S14V8_Falling_Delay_',
'course-v1:LinuxFoundationX+LFS101x.2+1T2015': 'block-v1:LinuxFoundationX+LFS101x.2+1T2015+type@video+block@07e47f483a6244ff807dfa28f2e9e205',
'course-v1:BerkeleyX+GG101x-2+1T2015': 'block-v1:BerkeleyX+GG101x-2+1T2015+type@video+block@c08ad531b212499f8d0692f2a35eade5',
'course-v1:MITx+6.002x_6x+1T2015': 'block-v1:MITx+6.002x_6x+1T2015+type@video+block@S14V6_Rising_Delay',
}


COURSE_ID_DICT = dict(
    SMALL_A=COURSE_ID_LIST_SMALL_A,
    SMALL_B=COURSE_ID_LIST_SMALL_B,
    MEDIUM_A=COURSE_ID_LIST_MEDIUM_A,
    MEDIUM_B=COURSE_ID_LIST_MEDIUM_B,
    LARGE_A=COURSE_ID_LIST_LARGE_A,
    LARGE_B=COURSE_ID_LIST_LARGE_B,
    XLARGE=COURSE_ID_LIST_XLARGE,
    SPLIT_A=SPLIT_COURSES_A
)
COURSE_ID_LIST = [
    "SMALL_A",
    "SMALL_B",
    "MEDIUM_A",
    "MEDIUM_B",
    "LARGE_A",
    "LARGE_B",
    "XLARGE",
    "SPLIT_A"
]

ALL_COURSES = COURSE_ID_LIST_XLARGE + SPLIT_COURSES_A
ALL_COURSES_STACK = COURSE_ID_LIST_XLARGE + SPLIT_COURSES_A
