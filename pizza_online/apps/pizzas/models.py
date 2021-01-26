from django.db import models
from pizza_online.apps.ingredients.models import Ingredient

class Pizza(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.99)
    added = models.DateField()
    status = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title
