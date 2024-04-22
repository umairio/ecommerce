# import random

from django.core.management.base import BaseCommand
from faker import Faker

# from store_app.constants import ProfileRole

fake = Faker("en_US")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # for _ in range(10):
        #     Category.objects.create(
        #         name=fake.word(),
        #     )
        # for _ in range(20):
        #     u = User.objects.create(
        #         email=fake.email(),
        #     )
        #     Profile.objects.create(
        #         user=u,
        #         phone_number=fake.phone_number(),
        #         role=random.choice(ProfileRole.ROLE),
        #     )
        # for _ in range(7):
        #     Shop.objects.create(
        #         name=fake.word(),
        #         owner=random.choice(
        #             Profile.objects.filter(role=ProfileRole.OWNER)
        #         ),
        #     )
        # for _ in range(50):
        #     shop = Shop.objects.all().order_by("?").first()
        #     seller = (
        #         Profile.objects.filter(role=ProfileRole.SELLER)
        #         .order_by("?")
        #         .first()
        #     )
        #     p = Product.objects.create(
        #         # capitalize it
        #         name=fake.word().capitalize(),
        #         price=random.randint(100, 1000),
        #         shop=shop,
        #         seller=seller,
        #         category=(Category.objects.all().order_by("?").first()),
        #     )
        #     Inventory.objects.create(
        #         product=p,
        #         total_quantity=random.randint(1, 10),
        #         shop=p.shop,
        #         seller=p.seller,
        #     )
        return
