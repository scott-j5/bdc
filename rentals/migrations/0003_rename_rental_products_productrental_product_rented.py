# Generated by Django 3.2.4 on 2021-07-20 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_auto_20210720_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productrental',
            old_name='rental_products',
            new_name='product_rented',
        ),
    ]