""" Constants used within tests """

COURSES = ['edX/DemoX/Demo_Course', 'CS/CS101/20432', 'MyOrganization/MC/2014_MC']

SEARCH_PHRASES = {
    'edX/DemoX/Demo_Course': [
        # Indexed phrases
        'Homework', 'School', 'Lila fisher', 'Exams', 'Social', 'Week 1', 'Video', 'Google',
        # Non-indexed phrases
        'Testing', 'Phrase', 'tomorrow', 'land of confusion'
    ],
    'CS/CS101/20432': [
        # Indexed phrases
        'SubsectionVideo', 'LILA FISHER', 'see the iframe specification', 'course info', 'see below', 'video subtitles',
        # Non-indexed phrases
        'search results', 'my xblock', 'discussion'
    ],
    'MyOrganization/MC/2014_MC': [
        # Indexed phrases
        'HTML', 'Introduction to HTML', 'Week 1', 'Components', 'Video', 'My Course', 'edX', 'ANANT AGARWAL',
        # Non-indexed phrases
        'Search', 'Tutorial', 'Documents', 'TIffany Smith'
    ],
}
