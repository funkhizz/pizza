import os
import random
from datetime import datetime

from django.dispatch import receiver
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save

from pizza_online.utils import unique_slug_generator
from pizza_online.apps.ingredients.models import Ingredient


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
    return f"pizzas/{date_time}/{title}/{final_filename}"


class Pizza(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.99)
    image = models.ImageField(upload_to=upload_image_path, blank=False, null=True)
    added = models.DateField()
    status = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pizza_detail", kwargs={"slug": self.slug})


@receiver(pre_save, sender=Pizza)
def pizza_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
