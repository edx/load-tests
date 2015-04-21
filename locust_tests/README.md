Locust Tests
============
The tests in this directory utilize the [Locust](http://docs.locust.io/en/latest/) load testing tool.

Getting Started
---------------
Get started by first installing Locust and any other prerequisites:

    $ pip install -r requirements.txt

Each service directory contains a `locustfile.py`. In order to run the tests, cd into the service directory and run the 
`locust` command as shown below. Remember to replace `<host>` with the hostname of the actual server being tested.

    $ locust --host=<host>


Some tests may rely on external data (e.g. auth credentials) being passed to the test via environment variables. See
the service's `locustfile.py` for details.
