# Generated by Django 3.2.4 on 2022-04-21 10:23

from django.db import migrations
import imageit.models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0008_rentalfulfilment__fulfilled_rental_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentaldriver',
            name='proof_of_address_1',
            field=imageit.models.ScaleItImageField(blank=True, upload_to=''),
        ),
    ]
