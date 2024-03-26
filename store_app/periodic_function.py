import os
import random
from io import BytesIO

from django.db.models import F, Sum
from faker import Faker
from reportlab.pdfgen import canvas

from .constants import OrderStatus, ProfileRole
from .models import Inventory, Order, Product, Profile, Review, Shop

fake = Faker()


def owner_report(owner):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    row_height = 16
    column_widths = [30, 170, 100]
    total_amount = 0
    shop = Shop.objects.get(owner=owner)
    # Define the data to be printed in the table
    order_data = [
        ["ID", "seller", "Total"],
    ]
    seller_ids = set(
        order.seller.id for order in Order.objects.filter(shop=shop.id)
    )
    for seller_id in seller_ids:
        order_data.append(
            [
                seller_id,
                Profile.objects.get(id=seller_id).user.email,
                Order.objects.filter(seller_id=seller_id).aggregate(
                    total=Sum("total_amount")
                )["total"],
            ]
        )
        total_amount += Order.objects.filter(seller_id=seller_id).aggregate(
            total=Sum("total_amount")
        )["total"]
    # Define pagination variables
    page_height = 830
    max_rows_per_page = 50
    current_row = 0
    current_page = 1

    # Generate pages
    while current_row < len(order_data):
        # Set up the page
        p.drawString(0, page_height, f"Owner: {shop.owner} - Shop: {shop.name}")

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
    p.drawString(450, 5, f"Total Amount: {total_amount}")
    # Save the PDF content to the buffer
    p.save()

    # Get the PDF content as bytes
    pdf_bytes = buffer.getvalue()

    # Save the PDF file locally
    pdf_path = os.path.join("reports/owner", f"Owner {owner}_data.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    return pdf_path


def seller_report(seller):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    row_height = 16
    column_widths = [30, 165, 130, 130, 50, 100]
    total_amount = 0

    # Define the data to be printed in the table
    order_data = [
        ["ID", "Buyer", "Shop", "Product", "Quantity", "Total"],
    ]
    for obj in Order.objects.filter(seller=seller):
        order_data.append(
            [
                obj.id,
                obj.buyer.user.email,
                obj.shop.name,
                obj.product.name,
                obj.quantity,
                obj.total_amount,
            ]
        )
        total_amount += obj.total_amount

    # Define pagination variables
    page_height = 830
    max_rows_per_page = 50
    current_row = 0
    current_page = 1

    # Generate pages
    while current_row < len(order_data):
        # Set up the page
        p.drawString(0, page_height, f"Page {current_page}")

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
    p.drawString(450, 5, f"Total Amount: {total_amount}")
    # Save the PDF content to the buffer
    p.save()

    # Get the PDF content as bytes
    pdf_bytes = buffer.getvalue()

    # Save the PDF file locally
    pdf_path = os.path.join("reports/seller", f"Seller_{seller}_data.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    return pdf_path


def buy_items():
    product = (
        Product.objects.filter(inventory_product__total_quantity__gte=3)
        .order_by("?")
        .first()
    )
    if product:
        quantity = random.randint(
            1, Inventory.objects.get(product=product).total_quantity
        )
        buyer = random.choice(Profile.objects.filter(role=ProfileRole.BUYER))
        order = Order.objects.create(
            buyer=buyer,
            product=product,
            shop=product.shop,
            quantity=quantity,
            seller=product.seller,
            total_amount=product.price * quantity,
            shipping_address=fake.address(),
            status=OrderStatus.DELIVERED,
        )
        Review.objects.create(
            order=order,
            reviewer=buyer,
            product=product,
            rating=random.randint(1, 5),
            comment=fake.sentence(),
        )
        Inventory.objects.filter(product=product).update(
            total_quantity=F("total_quantity") - quantity
        )
