Ecommerce Load Testing
======================

This directory contains Locust tasks designed to exercise ecommerce behavior on the LMS and the ecommerce service, referred to as "Otto." Currently, access to Otto is always through the LMS. If a user tries to enroll in a course on the LMS, the LMS makes a call to Otto which is responsible for creating and fulfilling an order for the corresponding product, ultimately resulting in an enrollment.

In order to run the tests, auto auth must be enabled on the LMS. In addition, the course modes used for testing must be associated with SKUs corresponding to products configured in Otto. For example, say the Demo course, with course ID `edX/DemoX.1/2014` is available on the LMS. In order to allow "purchases" of honor enrollments in the Demo course through Otto:

1. Use the Django admin on the LMS to set a SKU on the honor mode for the course with ID `edX/DemoX.1/2014`.
2. Create a new Seat product in Otto whose `course_key` attribute matches the course ID on the LMS, `edX/DemoX.1/2014`. Create a new variant of this product to represent the honor mode on the LMS, and add a stock record for this variant whose SKU matches the SKU set previously on the LMS.

The tests support the following environment variables:

| Variable(s)                      | Required? | Description                                                |
|----------------------------------|-----------|------------------------------------------------------------|
| BASIC_AUTH_USER, BASIC_AUTH_PASS | No        | Credentials to use for basic access authentication         |
| LOCUST_TASK_SET                  | No        | TaskSet to run; must be imported into the locustfile       |
| COURSE_ID                        | No        | ID of a course with a SKU on its honor mode                |
| SKU                              | No        | SKU corresponding to a product with a non-zero price       |
| ECOMMERCE_SERVICE_URL            | No        | URL root for the ecommerce service                         |
| ECOMMERCE_API_SIGNING_KEY        | No        | Key to use when signing JWTs sent to the ecommerce service |
| CYBERSOURCE_SECRET_KEY           | No        | Key to use when signing CyberSource transaction parameters |

Note that if you want to use the defaults provided for these variables - in particular, `ECOMMERCE_API_SIGNING_KEY` and `CYBERSOURCE_SECRET_KEY` - you will need to ensure that these defaults are configured across the LMS and Otto.
