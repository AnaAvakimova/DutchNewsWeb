from .base import *

DEBUG = True
ALLOWED_HOSTS = ['89.116.243.80', 'localhost', '127.0.0.1', 'your_server_ip']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')