from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class BaseDiscount(BaseModel):
    DISCOUNT_TYPE_PRODUCT = "discount"
    DISCOUNT_TYPE_ORDER = "order"

    TYPE_CHOICES = (
        (_("تخفیف درصدی"), ),
        (_("تخفیف عددی"), ),
    )

    #   TODO:implement flag choices in children classes
    FLAG_CHOICES = (
        ...
    )

    amount = models.PositiveIntegerField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=100)
    flag = models.CharField(choices=FLAG_CHOICES, max_length=100)
