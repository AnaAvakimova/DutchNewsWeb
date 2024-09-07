from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
