import os
from celery import Celery
from django.conf import settings

# Configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BongobetBackend.settings')

app = Celery('BongobetBackend', broker='amqp://',
             backend='rpc://',
             include=['BongobetBackend.tasks'])

# Configurações do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()