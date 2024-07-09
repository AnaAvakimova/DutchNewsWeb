from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
