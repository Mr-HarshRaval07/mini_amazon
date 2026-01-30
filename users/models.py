from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter a valid Indian mobile number (10 digits starting with 6-9)"
)

class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    full_name = models.CharField(max_length=200, blank=True)

    phone = models.CharField(
        validators=[phone_regex],
        max_length=10,
        blank=True
    )

    phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True)

    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

