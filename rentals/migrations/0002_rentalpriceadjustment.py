# Generated by Django 3.2.4 on 2021-07-20 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0001_initial'),
        ('rentals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalPriceAdjustment',
            fields=[
                ('priceadjustment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='invoicing.priceadjustment')),
                ('rentals', models.ManyToManyField(to='rentals.ProductRental')),
            ],
            bases=('invoicing.priceadjustment',),
        ),
    ]
