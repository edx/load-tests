"""Configuration shared across ecommerce tasks."""
import os

# ID of a course on the LMS with a SKU on its honor mode
COURSE_ID = 'edX/DemoX.1/2014'

BASKET_ID = os.environ.get('BASKET_ID', 1)
CYBERSOURCE_SECRET_KEY = os.environ.get('CYBERSOURCE_SECRET_KEY')
ECOMMERCE_SERVICE_URL = os.environ.get('ECOMMERCE_SERVICE_URL', 'http://localhost:8002').strip('/')
ECOMMERCE_API_URL = os.environ.get('ECOMMERCE_API_URL', '{}/api/v2'.format(ECOMMERCE_SERVICE_URL)).strip('/')
ECOMMERCE_API_SIGNING_KEY = os.environ.get('ECOMMERCE_API_SIGNING_KEY')
SKU = os.environ.get('SKU', 'SEAT-HONOR-EDX-DEMOX-DEMO-COURSE')

LMS_USERNAME = os.environ.get('LMS_USERNAME')
LMS_EMAIL = os.environ.get('LMS_EMAIL')
