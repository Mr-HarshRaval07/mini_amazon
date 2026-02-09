import json
from products.models import Product, Category
from orders.models import Order, OrderItem
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

User = get_user_model()

def admin_dashboard_context(request):

    if not request.user.is_staff:
        return {}

    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    users_count = User.objects.count()

    paid_orders = Order.objects.filter(status="Paid")

    total_revenue = paid_orders.aggregate(
        Sum("total_price")
    )["total_price__sum"] or 0

    sales_by_day = (
        paid_orders
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Sum("total_price"))
        .order_by("day")
    )

    orders_by_day = (
        paid_orders
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # ✅ CONVERT TO JSON STRING

    sales_data = [
    {"day": str(x["day"]), "total": float(x["total"])}
    for x in sales_by_day
]

    orders_data = [
    {"day": str(x["day"]), "count": x["count"]}
    for x in orders_by_day
]


    best_product = (
        OrderItem.objects
        .values("product__name")
        .annotate(qty=Sum("quantity"))
        .order_by("-qty")
        .first()
    )

    insight = "📈 Keep growing!"

    return {
        "products_count": products_count,
        "categories_count": categories_count,
        "users_count": users_count,

        "total_revenue": total_revenue,
        "best_product": best_product,

        "sales_data": sales_data,
        "orders_data": orders_data,

        "insight": insight
    }
