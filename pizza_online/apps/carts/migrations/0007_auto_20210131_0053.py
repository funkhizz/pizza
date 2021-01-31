# Generated by Django 3.1.5 on 2021-01-31 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0001_initial"),
        ("carts", "0006_cartitem_extra_ingredients"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="price",
            field=models.DecimalField(decimal_places=2, default=12.99, max_digits=5),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="extra_ingredients",
            field=models.ManyToManyField(blank=True, to="ingredients.Ingredient"),
        ),
    ]
