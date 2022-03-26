# Generated by Django 3.2.4 on 2022-03-25 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_rentalproduct_rentable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentalfulfilment',
            old_name='rental_price',
            new_name='rental_base_price',
        ),
        migrations.AlterField(
            model_name='rentalfulfilment',
            name='rental_extras',
            field=models.ManyToManyField(blank=True, to='rentals.RentalExtra'),
        ),
    ]
