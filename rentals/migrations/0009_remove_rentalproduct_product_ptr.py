# Generated by Django 3.2.4 on 2021-07-22 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0008_rentalproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalproduct',
            name='product_ptr',
        ),
    ]
