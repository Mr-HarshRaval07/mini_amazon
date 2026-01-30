from products.models import Product, Review, Category
from django.contrib.auth.models import User

def admin_dashboard_context(request):
    return {
        "products_count": Product.objects.count(),
        "reviews_count": Review.objects.count(),
        "categories_count": Category.objects.count(),
        "users_count": User.objects.count(),
    }
