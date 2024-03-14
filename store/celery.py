from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")
app = Celery("store")
app.conf.enable_utc = False
app.config_from_object(settings, namespace="CELERY")
app.conf.beat_schedule = {
    "buy": {"task": "store_app.tasks.buy_items_from_shop", "schedule": 10},
    "add_stock": {"task": "store_app.tasks.add_stock", "schedule": 10},
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
