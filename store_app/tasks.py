import random

from celery import Celery, shared_task
from django.db.models import F
from faker import Faker
from django.http import HttpResponse
import os
from reportlab.pdfgen import canvas
from io import BytesIO

from .models import Inventory, Order, Product, Profile, Shop

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

@shared_task(bind=True)
def generate_shop_report(self):
    for shop in Shop.objects.all():
        generate_pdf(shop.id)

def generate_pdf(shop):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    row_height = 16
    column_widths = [30, 165, 150, 130, 50, 100]
    total_amount = 0

    # Define the data to be printed in the table
    order_data = [
        ['ID', 'Buyer', 'Seller', 'Product', 'Quantity', 'Total'],
    ]
    for obj in Order.objects.filter(shop=shop):
        order_data.append([
            obj.id,
            obj.buyer.user.email,
            obj.seller.user.email,
            obj.product.name,
            obj.quantity,
            obj.total_amount,
        ])
        total_amount += obj.total_amount

    # Define pagination variables
    page_height = 830
    max_rows_per_page = 50
    current_row = 0
    current_page = 1

    # Generate pages
    while current_row < len(order_data):
        # Set up the page
        p.drawString(0, page_height, f'Page {current_page}')

        # Draw rows on the page
        x = 10
        y = page_height - 20
        for row in order_data[current_row:current_row + max_rows_per_page]:
            for i in range(len(row)):
                p.drawString(x, y, str(row[i]))
                x += column_widths[i]
            x = 10
            y -= row_height
        current_row += max_rows_per_page
        current_page += 1

        # If there are more rows, add a new page
        if current_row < len(order_data):
            p.showPage()
    # entering total amout at the end of page
    p.drawString(450, 5, f'Total Amount: {total_amount}')
    # Save the PDF content to the buffer
    p.save()

    # Get the PDF content as bytes
    pdf_bytes = buffer.getvalue()

    # Save the PDF file locally
    pdf_path = os.path.join(f'shop_{shop}_data.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes)

    return pdf_path
