import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pitter.settings')

application = get_wsgi_application()  # pylint: disable=invalid-name

