"""
WSGI config for DutchNewsWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.path.isfile(os.path.join(os.path.dirname(__file__), 'local_settings.py')):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DutchNewsWeb.settings.development")

application = get_wsgi_application()
