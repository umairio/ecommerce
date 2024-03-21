from celery import shared_task
from django.db.models import F

from .models import Inventory, Profile, Shop
from .periodic_function import buy_items, seller_report, shop_report


@shared_task(bind=True)
def buy_items_from_shop(self):
    buy_items()


@shared_task(bind=True)
def add_stock(self):
    Inventory.objects.filter(total_quantity__lte=3).update(
        total_quantity=F("total_quantity") + 10
    )


@shared_task(bind=True)
def generate_shop_report(self):
    for shop in Shop.objects.all():
        shop_report(shop.id)


@shared_task(bind=True)
def generate_seller_report(self):
    for seller in Profile.objects.filter(role="seller"):
        seller_report(seller.id)
