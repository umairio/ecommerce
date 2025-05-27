from celery import shared_task
from django.db.models import F

from .models import Inventory, Profile
from .periodic_function import buy_items, owner_report, seller_report


@shared_task(bind=True)
def buy_items_from_shop(self):
    buy_items()


@shared_task(bind=True)
def add_stock(self):
    Inventory.objects.filter(total_quantity__lte=3).update(
        total_quantity=F("total_quantity") + 10
    )


@shared_task(bind=True)
def generate_owner_report(self):
    for owner in Profile.objects.filter(role="owner"):
        owner_report(owner.id)


@shared_task(bind=True)
def generate_seller_report(self):
    for seller in Profile.objects.filter(role="seller"):
        seller_report(seller.id)
