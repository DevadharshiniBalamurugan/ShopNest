import os
from django.core.management import call_command
from django.db import OperationalError, ProgrammingError
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','shopnest.settings')
application=get_wsgi_application()

try:
	from store.models import Product
	if not Product.objects.exists():
		call_command('seed_data', verbosity=0)
except (OperationalError, ProgrammingError):
	pass
