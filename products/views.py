from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from decimal import Decimal, InvalidOperation

from django.db import models
from django.db.models import Avg

from .models import Product, RecentlyViewed, Wishlist, Review
from products.models import Category


# ================= ADD REVIEW =================

@login_required
def add_review(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                "rating": rating,
                "comment": comment
            }
        )

    return redirect("product_detail", pk=product_id)


# ================= WISHLIST TOGGLE =================

@login_required
def toggle_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)   # FIXED

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.warning(request, "Removed from wishlist ❤️")
    else:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )
        messages.success(request, "Added to wishlist ❤️")

    return redirect(request.META.get("HTTP_REFERER", "/"))


# ================= PRODUCT DETAIL =================

def product_detail(request, pk):

    product = get_object_or_404(
        Product.objects.prefetch_related("images"),
        pk=pk
    )

    # 👁️ Increment views safely
    Product.objects.filter(id=product.id).update(
        views=models.F("views") + 1
    )

    # -------- Recently Viewed --------
    if request.user.is_authenticated:

        RecentlyViewed.objects.filter(
            user=request.user,
            product=product
        ).delete()

        RecentlyViewed.objects.create(
            user=request.user,
            product=product
        )

        # keep latest 5 only
        old_items = RecentlyViewed.objects.filter(
            user=request.user
        ).order_by("-viewed_at")[5:]

        if old_items.exists():
            old_items.delete()

    # -------- Recommendations --------
    recommendations = Product.objects.prefetch_related("images").filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    # -------- Reviews --------
    reviews = Review.objects.filter(product=product).order_by("-created_at")

    avg_rating = reviews.aggregate(
        avg=Avg("rating")
    )["avg"] or 0

    return render(request, "products/detail.html", {
        "product": product,
        "recommendations": recommendations,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1)
    })


# ================= HOME PAGE =================

def home(request):

    selected_category = request.GET.get("category")

    products = Product.objects.prefetch_related("images")

    # 📂 Category filter
    if selected_category and selected_category.isdigit():
        products = products.filter(category_id=int(selected_category))

    # 💰 Price filter
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    try:
        if min_price:
            products = products.filter(price__gte=Decimal(min_price))
    except:
        pass

    try:
        if max_price:
            products = products.filter(price__lte=Decimal(max_price))
    except:
        pass

    # 🔃 Sorting
    sort = request.GET.get("sort")

    if sort == "low":
        products = products.order_by("price")
    elif sort == "high":
        products = products.order_by("-price")
    elif sort == "new":
        products = products.order_by("-id")

    # 📄 Pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page", 1)
    products = paginator.get_page(page_number)

    categories = Category.objects.all()


    # 🔥 POPULAR (CATEGORY BASED)
    popular_products = Product.objects.prefetch_related("images")

    if selected_category and selected_category.isdigit():
        popular_products = popular_products.filter(category_id=int(selected_category))

    popular_products = popular_products.order_by("-views")[:4]


    # 🕒 RECENTLY VIEWED (CATEGORY BASED)
    recent_products = []

    if request.user.is_authenticated:

        recent_products = RecentlyViewed.objects.select_related(
            "product"
        ).prefetch_related(
            "product__images"
        ).filter(user=request.user)

        if selected_category and selected_category.isdigit():
            recent_products = recent_products.filter(
                product__category_id=int(selected_category)
            )

        recent_products = recent_products[:5]


    return render(request, "products/home.html", {
        "products": products,
        "categories": categories,
        "popular_products": popular_products,
        "recent_products": recent_products
    })



# ================= WISHLIST PAGE =================

@login_required
def wishlist_page(request):

    items = Wishlist.objects.select_related(
        "product"
    ).prefetch_related(
        "product__images"
    ).filter(user=request.user)

    return render(request, "products/wishlist.html", {
        "items": items
    })
