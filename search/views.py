from django.http import JsonResponse
from django.shortcuts import render
from products.models import Product, Category, RecentlyViewed
from django.core.paginator import Paginator


# ================= AUTOCOMPLETE =================

def autocomplete(request):
    q = request.GET.get('q', '').strip()

    products = Product.objects.filter(name__icontains=q)[:5]

    data = [{"id": p.id, "name": p.name} for p in products]

    return JsonResponse(data, safe=False)


# ================= SEARCH + FILTER + AUTO RECOMMEND =================

def search_results(request):

    products = Product.objects.all()

    # 🔍 SEARCH
    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)

    # 📂 CATEGORY
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # 💰 PRICE FILTER
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # 🔃 SORT
    sort = request.GET.get('sort')

    if sort == "low":
        products = products.order_by('price')

    elif sort == "high":
        products = products.order_by('-price')

    # 📄 PAGINATION
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # 📁 CATEGORIES
    categories = Category.objects.order_by('name')

    # ================= AUTO RECOMMENDATION =================

    # Recently viewed (user based)
    recent_products = []

    if request.user.is_authenticated:
        recent_products = (
            RecentlyViewed.objects
            .filter(user=request.user)
            .select_related('product')
            .order_by('-viewed_at')[:6]
        )

    # Popular products (based on views)
    popular_products = Product.objects.order_by('-views')[:6]

    # =======================================================

    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
        'recent_products': recent_products,
        'popular_products': popular_products
    })
