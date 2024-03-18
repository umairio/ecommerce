import random

from celery import Celery, shared_task
from django.db.models import F
from faker import Faker

from .models import Inventory, Order, Product, Profile

app = Celery("tasks", broker="redis://localhost:6379")


fake = Faker()


@shared_task(bind=True)
def buy_items_from_shop(self):
    product = (
        Product.objects.filter(inventory__total_quantity__gte=3)
        .order_by("?")
        .first()
    )
    if product:
        quantity = random.randint(
            1, Inventory.objects.get(product=product).total_quantity
        )
        Order.objects.create(
            buyer=random.choice(
                Profile.objects.filter(role=Profile.Role.Buyer)
            ),
            product=product,
            shop=product.shop,
            quantity=quantity,
            seller=product.seller,
            total_amount=product.price * quantity,
            shipping_address=fake.address(),
        )
        Inventory.objects.filter(product=product).update(
            total_quantity=F("total_quantity") - quantity
        )


@shared_task(bind=True)
def add_stock(self):
    Inventory.objects.filter(total_quantity__lte=3).update(
        total_quantity=F("total_quantity") + 10
    )


# @app.task
# def create_prod_inventory():
#     for _ in range(50):
#         Product.objects.create(
#             name = fake.name(),
#             description = fake.text(),
#             price = random.randint(100, 1000),
#             category = random.choice(Category.objects.all()),
#             seller = random.choice(
#                 Profile.objects.filter(role=Profile.Role.Seller)),
#             shop = random.choice(Shop.objects.all()),
#             rating = random.randint(0, 5),
#         )
#     for product in Product.objects.all():
#         Inventory.objects.create(
#             shop = product.shop,
#             product = product,
#             seller = product.seller,
#             total_quantity = random.randint(5, 15),
#         )
#     for product in Product.objects.all():
#         product.name = fake.word().capitalize() + ' ' + fake.word()
#         product.save()
