# Generated by Django 3.1.5 on 2021-01-29 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='line_total',
        ),
    ]