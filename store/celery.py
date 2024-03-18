from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")
app = Celery("store")
app.conf.enable_utc = False
app.config_from_object(settings, namespace="CELERY")
app.conf.beat_schedule = {
    # "buy": {"task": "store_app.tasks.buy_items_from_shop", "schedule": 10},
    # "add_stock": {"task": "store_app.tasks.add_stock", "schedule": 10},
    "daily_sale_report": {
        "task": "store_app.tasks.generate_shop_report",
        "schedule": crontab(hour=0),
    },
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
