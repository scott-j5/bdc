# Generated by Django 3.2.4 on 2022-04-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0015_rentalfulfilment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalfulfilment',
            name='pickup_location',
            field=models.CharField(blank=True, help_text='Leave blank if not required', max_length=100, null=True),
        ),
    ]