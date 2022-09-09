import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(verbose_name=_("phone number"), max_length=11)
    profile_image = models.FileField(verbose_name=_("profile image"),
                                     upload_to="customers/profile_pics/",
                                     default="default_images/user.png")
    identifier_phone = models.CharField(verbose_name=_("identifier phone number"), max_length=11, null=True, blank=True)

    def __str__(self):
        return self.phone_number
