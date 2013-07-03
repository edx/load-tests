load-tests
==========
Load tests for the edX platform, currently only in multimechanize.


Installation
------------

This code runs on Python 2.7.

1.  Get a local copy of this repo.

2.  (Optional)  Create and activate a virtualenv to work in.

3.  Install the requirements (you may need to sudo this if you don't use virtualenv)
    a) I had to do these by hand rather than via pip to get loremipsum installed:

        $ curl -O http://python-distribute.org/distribute_setup.py
        $ python distribute_setup.py

    b) Now download loremipsum, install it with: python setup.py install

    c) I also needed to install numpy separately

        $ pip install numpy

    d) Now the rest of the requirements install cleanly
        $ pip install -r requirements.txt


Execution
---------
Run the scripts with the multimech-run command. The lms tests take command line arguments:

```
multimech-run edx-platform/lms/ username password org coursename runtime
```

Example:
```
multimech-run edx-platform/lms/ test@edx.org test MITx 6.00x 2013_Spring
```
