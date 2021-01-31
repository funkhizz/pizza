# Generated by Django 3.1.5 on 2021-01-30 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0001_initial"),
        ("carts", "0005_remove_cart_products"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="extra_ingredients",
            field=models.ManyToManyField(to="ingredients.Ingredient"),
        ),
    ]
