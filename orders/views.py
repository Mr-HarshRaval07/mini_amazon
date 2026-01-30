import re

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .models import Order, OrderItem, CartItem


# ================= ADD TO CART =================

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))


# ================= VIEW CART =================

@login_required
def view_cart(request):

    items = CartItem.objects.select_related("product").filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "orders/cart.html", {
        "items": items,
        "total": total
    })


# ================= UPDATE CART =================

@login_required
def update_cart(request, item_id, action):

    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if action == "plus":
        item.quantity += 1

    elif action == "minus":
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect("/orders/cart/")

    elif action == "remove":
        item.delete()
        return redirect("/orders/cart/")

    item.save()
    return redirect("/orders/cart/")


# ================= CHECKOUT =================

@login_required
@transaction.atomic
def checkout(request):

    items = CartItem.objects.select_related("product").filter(user=request.user)

    if not items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("/orders/cart/")

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        # ✅ Required fields
        if not full_name or not email or not phone or not address:
            messages.error(request, "All fields required")
            return redirect("/orders/checkout/")

        # 📱 Indian phone validation
        if not re.match(r'^[6-9]\d{9}$', phone):
            messages.error(request, "Enter valid 10 digit Indian mobile number")
            return redirect("/orders/checkout/")

        # ================= STOCK CHECK FIRST =================

        for item in items:
            if item.product.inventory < item.quantity:
                messages.error(
                    request,
                    f"Not enough stock for {item.product.name}"
                )
                return redirect("/orders/cart/")

        # ================= CREATE ORDER =================

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            status="Paid"
        )

        total_items = 0
        total_price = 0

        for item in items:

            product = Product.objects.select_for_update().get(id=item.product.id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price_at_purchase=product.price
            )

            product.inventory -= item.quantity
            product.save()

            total_items += item.quantity
            total_price += product.price * item.quantity

        # ✅ Save totals
        order.total_items = total_items
        order.total_price = total_price
        order.save()

        # 🧹 Clear cart
        items.delete()

        messages.success(request, "Order placed successfully 🎉")

        return redirect("/orders/my-orders/")

    return render(request, "orders/checkout.html", {
        "items": items
    })


# ================= MY ORDERS =================

@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })


# ================= ORDER DETAIL =================

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "orders/order_detail.html", {
        "order": order
    })
