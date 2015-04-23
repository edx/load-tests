"""Configuration shared across ecommerce tasks."""
import os


# ID of a course with a SKU on its honor mode
COURSE_ID = os.environ.get('COURSE_ID', 'edX/DemoX.1/2014')

# SKU corresponding to a product with a non-zero price. Must be associated with
# a verified or professional mode.
SKU = os.environ.get('SKU', 'default-sku')

ECOMMERCE_SERVICE_URL = os.environ.get(
    'ECOMMERCE_SERVICE_URL',
    'http://localhost:8002'
).strip('/')

ECOMMERCE_API_URL = os.environ.get(
    'ECOMMERCE_API_URL',
    '{}/api/v2'.format(ECOMMERCE_SERVICE_URL)
).strip('/')

ECOMMERCE_API_SIGNING_KEY = os.environ.get('ECOMMERCE_API_SIGNING_KEY', 'insecure-secret-key')
CYBERSOURCE_SECRET_KEY = os.environ.get('CYBERSOURCE_SECRET_KEY', 'insecure-secret-key')

