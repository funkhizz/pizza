# Generated by Django 3.1.5 on 2021-01-26 23:18

from django.db import migrations, models
import pizza_online.apps.pizzas.models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0004_pizza_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(null=True, upload_to=pizza_online.apps.pizzas.models.upload_image_path),
        ),
    ]
