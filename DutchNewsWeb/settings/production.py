from .base import *

DEBUG = False
ALLOWED_HOSTS = ['89.116.243.80']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')