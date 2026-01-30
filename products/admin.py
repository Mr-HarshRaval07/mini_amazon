from django.contrib import admin
from .models import Product, Category, ProductImage, Review


# ================= PRODUCT IMAGES INLINE =================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1   # shows 1 empty upload field


# ================= PRODUCT ADMIN =================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ("search_vector",)

    list_display = ("name", "price", "views")
    search_fields = ("name",)
    list_filter = ("price",)

    inlines = [ProductImageInline]


# ================= PRODUCT IMAGE =================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")
    list_filter = ("product",)


# ================= CATEGORY =================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


# ================= REVIEW =================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("comment",)
