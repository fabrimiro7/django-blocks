from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Imposta il modulo di configurazione per Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edplatform.settings')

app = Celery('edplatform')

# Usa il prefisso di configurazione Celery da Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carica i task registrati in tutti i moduli task di Django app
app.autodiscover_tasks()

