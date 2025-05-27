class ProfileRole:
    ADMIN = "admin"
    OWNER = "owner"
    BUYER = "buyer"
    SELLER = "seller"

    ROLE = (
        (ADMIN, "admin"),
        (OWNER, "owner"),
        (BUYER, "buyer"),
        (SELLER, "seller"),
    )


class OrderStatus:
    CART = "cart"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

    STATUS = (
        (CART, "cart"),
        (CONFIRMED, "confirmed"),
        (SHIPPED, "shipped"),
        (DELIVERED, "delivered"),
    )
