Ecommerce Load Testing
======================

This directory contains Locust tasks designed to exercise ecommerce behavior on the LMS and the ecommerce service, referred to as "Otto." Currently, access to Otto is always through the LMS. If a user tries to enroll in a course on the LMS, the LMS makes a call to Otto which is responsible for creating and fulfilling an order for the corresponding product, ultimately resulting in an enrollment.

In order to run the tests, auto auth must be enabled on the LMS. In addition, the course modes used for testing must be associated with SKUs corresponding to products configured in Otto. For example, say the Demo course, with course ID `edX/DemoX.1/2014` is available on the LMS. In order to allow "purchases" of honor enrollments in the Demo course through Otto:

1. Use the Django admin on the LMS to set a SKU on the honor mode for the course with ID `edX/DemoX.1/2014`.
2. Create a new Seat product in Otto whose `course_key` attribute matches the course ID on the LMS, `edX/DemoX.1/2014`. Create a new variant of this product to represent the honor mode on the LMS, and add a stock record for this variant whose SKU matches the SKU set previously on the LMS.

The tests support the following environment variables:

| Variable(s)                      | Description                                                                             |
|----------------------------------|-----------------------------------------------------------------------------------------|
| BASIC_AUTH_USER, BASIC_AUTH_PASS | If set, will be used for HTTP authentication                                            |
| LOCUST_TASK_SET                  | If set, the specified TaskSet will be run; it must first be imported into the locustfile|
