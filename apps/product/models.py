import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.core.models import BaseModel, BaseDiscount


class Product(BaseModel):
    uid = models.CharField(verbose_name=_("uid"), default=uuid.UUID, unique=True, max_length=64)
    eng_name = models.CharField(verbose_name=_("english name"), max_length=100)
    fa_name = models.CharField(verbose_name=_("persian name"), max_length=100)
    price = models.PositiveIntegerField(verbose_name=_("price"))
    is_available = models.BooleanField(verbose_name=_("is available"), default=True)
    stock = models.PositiveIntegerField(verbose_name=_("stock"))

    def __str__(self):
        return self.uid


class OrderDiscount(BaseDiscount):
    pass


class ProductDiscount(BaseDiscount):
    pass


class SpecialDiscount(BaseDiscount):
    pass


class Provider(BaseModel):
    pass
