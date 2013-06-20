load-tests
==========
Load tests for the edX platform, currently only in multimechanize.  

Folders:  

mechanize/edx-platform/lms/test_scripts LMS API calls to forum posts, login, register, etc.  

How to use:  
multimech-run lms/ username password org coursename runtime  
Example:  
multimech-run lms/ test@edx.org test MITx 6.00x 2013_Spring  
  
Requirements:  
Mechanize http://wwwsearch.sourceforge.net/mechanize/  
matplotlib (if you wish to plot the results)http://matplotlib.org/  
Multi-mechanize http://testutils.org/multi-mechanize/  
loremipsum (https://pypi.python.org/pypi/loremipsum)  

