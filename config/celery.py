import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = os.getenv("REDIS")
app.conf.result_backend = os.getenv("REDIS")
app.autodiscover_tasks()
