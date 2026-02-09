from django.db import models
from django.conf import settings
from products.models import Product


# =====================
# CART ITEM
# =====================

class CartItem(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="in_carts"
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "product")
        indexes = [
            models.Index(fields=["user"]),
        ]

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user} | {self.product.name} x {self.quantity}"


# =====================
# ORDER
# =====================

class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_CHOICES = [
        ("QR", "QR Payment"),
        ("CARD", "Card Payment"),
        ("COD", "Cash On Delivery"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # 🔥 ORDER STATUS
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    # 💳 PAYMENT FIELDS (NEW)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        default="Pending"
    )

    total_items = models.PositiveIntegerField(default=0)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),  # ⚡ faster filtering
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"



# =====================
# ORDER ITEM
# =====================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ordered_items"
    )

    quantity = models.PositiveIntegerField()

    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
