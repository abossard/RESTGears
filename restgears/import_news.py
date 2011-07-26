from djangoappengine.main import main
from django.conf import settings

from django.core import management
management.call_command('import_news',)
