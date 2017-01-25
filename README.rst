Repository Usage
================

The ``analysis/`` directory is for holding individual datasets and processed
results obtained from load testing.  Keep each project under subdirectories
named after the corresponding JIRA issue, e.g. ``analysis/PERF-404``.

Please try to make your results reproducable.  Commit your Jupyter (ipython)
notebooks, python scripts, ``INSTRUCTIONS.rst`` files, etc.

History
=======

This repository used to contain code for edx load tests.  Those have since been
removed, and a subset of them migrated to the public edx/edx-load-tests_ repo.

.. _edx-load-tests: https://github.com/edx/edx-load-tests/

Refer to the ``old-tests`` branch of this repository for a snapshot of those
deprecated tests.
