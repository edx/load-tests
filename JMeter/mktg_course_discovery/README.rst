Course Discovery Performance Tests
----------------------------------

These are the performance tests for the marketing site's "course discovery" feature.


Configuring the Tests
=====================

You can configure the test server URL, basic auth credentials, rampup time,
and connection timeout.

1. Install and start JMeter_.
2. Open ``test/mktg-course-discovery.jmx`` in JMeter.
3. Edit "User Defined Variables"
4. Save the test.


Running Tests Locally
=====================

1. Install and start JMeter_.
2. Generate the test data:

.. code:: bash

    ./generate_data.py

3. Open ``test/mktg-course-discovery.jmx`` in JMeter.
4. Click "Run" and view the results in "Summary Report" or "View Results Tree"


Running Tests in Blazemeter
===========================

To run the test at scale, we use Blazemeter_.

1. Log into Blazemeter.  If you don't have access, ask DevOps.
2. Create a new test and upload all the files in the ``test/`` directory.
3. Choose the number of engines and number of threads per engine.
4. Run the test.


.. _JMeter: http://jmeter.apache.org/
.. _Blazemeter: http://blazemeter.com/


Test Design
===========

The test divides traffic roughly equally between these groups:

1. High-traffic pages (homepage, course lists): ``input/primary_urls.csv``
2. Low-traffic pages: ``input/secondary_urls.csv``
3. Search
4. Autocomplete subject
5. Autocomplete school
6. Autocomplete course

The data generation script:

* Randomizes URLs
* Adds search terms with typographical errors (insertion of one additional character randomly in the term)
* Adds partial terms for auto-complete (e.g. "discrete" --> "d", "di", "dis", "disc", "discr", etc.)

Search terms and URLs are based on data from Google Analytics.
