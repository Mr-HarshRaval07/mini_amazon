import json
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

from orders.models import Order, OrderItem


@staff_member_required
def admin_dashboard(request):

    # ✅ Only paid orders
    orders = Order.objects.filter(status="Paid")

    # 📈 Sales per day
    sales_by_day = (
        orders
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Sum("total_price"))
        .order_by("day")
    )

    # 📦 Orders per day
    orders_by_day = (
        orders
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # 💰 Total revenue
    total_revenue = orders.aggregate(
        Sum("total_price")
    )["total_price__sum"] or 0

    # 📊 Total orders
    total_orders = orders.count()

    # 🔥 Top selling products
    top_products = (
        OrderItem.objects
        .values("product__name")
        .annotate(qty=Sum("quantity"))
        .order_by("-qty")[:5]
    )

    # 🧠 AI-style insight (simple logic)
    insight = "Sales are stable."

    if sales_by_day.count() >= 2:
        first = sales_by_day[0]["total"]
        last = sales_by_day.last()["total"]

        if last > first:
            insight = "📈 Sales are increasing!"
        elif last < first:
            insight = "📉 Sales are decreasing!"

    # ✅ Convert sales data to JSON for JS
    sales_data_json = json.dumps([
        {
            "day": str(item["day"]),
            "total": float(item["total"])
        }
        for item in sales_by_day
    ])

    orders_data_json = json.dumps([
    {
        "day": str(item["day"]),
        "count": item["count"]
    }
    for item in orders_by_day
])

    context = {
    "sales_data": sales_data_json,
    "orders_data": orders_data_json,
    "total_orders": total_orders,
    "total_revenue": total_revenue,
    "top_products": top_products,
    "insight": insight
}


    return render(request, "analytics/dashboard.html", context)
