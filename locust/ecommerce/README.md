Ecommerce Locust Tests
========================
The tests in this directory utilize the [Locust](http://docs.locust.io/en/latest/) load testing tool.

Getting Started
---------------
Get started by first installing Locust and any other prerequisites:

    $ pip install -r requirements.txt

This directory contains a `locustfile.py`. In order to run the tests, cd into the service directory and run the 
`locust` command as shown below. Remember to replace `<host>` with the hostname of the actual server being tested.

    $ locust --host=<host>


Settings
---------
In order to run these tests, you will need to set the JWT_SECRET environment variable in order to access the ecommerce application endpoint.

In addition, you may or may not also need to set basic auth credentials depending on the server you are testing against. You can set these credentials using the environment variables BASIC_AUTH_USER and BASIC_AUTH_PASSWORD. 
