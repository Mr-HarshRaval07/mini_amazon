from django.urls import path
from .views import autocomplete, search_results

urlpatterns = [
    path('autocomplete/', autocomplete),
    path('results/', search_results),
]
