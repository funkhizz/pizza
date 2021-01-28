import os
import random
from datetime import datetime

from django.dispatch import receiver
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save

from pizza_online.utils import unique_slug_generator
from pizza_online.apps.ingredients.models import Ingredient
from .choices import CATEGORY_CHOICES


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    date_time = datetime.now().strftime("%Y-%m-%d")
    title = instance.title.replace(" ", "")
    new_filename = random.randint(1, 5000000)
    name, ext = get_filename_ext(filename)
    final_filename = f"{name}{ext}"
    return f"products/{date_time}/{title}/{final_filename}"


class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=15.99)
    image = models.ImageField(upload_to=upload_image_path, blank=False, null=True)
    added = models.DateField()
    status = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="1")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:pizza-detail", kwargs={"slug": self.slug})


@receiver(pre_save, sender=Product)
def product_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
