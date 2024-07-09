from .base import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = False
ALLOWED_HOSTS = ['89.116.243.80', 'sketch.news', 'www.sketch.news']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')