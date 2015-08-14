import sys

sys.path.append("/home/alawi/edx/orphans/edx-platform")

from lms.envs.devplus import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edxapp',
        'USER': 'edxapp',
        'PASSWORD': 'password',
        'PORT': '3306',
    }
}
