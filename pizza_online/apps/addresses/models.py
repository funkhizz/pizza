from django.db import models
from pizza_online.apps.billing.models import BillingProfile


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    company = models.CharField(max_length=120, blank=True, null=True)
    address_1 = models.CharField(max_length=120)
    address_2 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    post_code = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return str("{0}, {1}, {2}".format(self.address_1, self.city, self.post_code))
