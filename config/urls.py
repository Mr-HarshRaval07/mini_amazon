from django.contrib import admin
from django.urls import path, include

from django.conf import settings          # ✅ ADD
from django.conf.urls.static import static # ✅ ADD

urlpatterns = [
    path('', include('products.urls')),
    path('', include('users.urls')),   # 👈 THIS LINE REQUIRED
    path('orders/', include('orders.urls')),
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls),
]


# ✅ ADD THIS AT VERY BOTTOM
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
