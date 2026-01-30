from django.db import models
from django.conf import settings

class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
