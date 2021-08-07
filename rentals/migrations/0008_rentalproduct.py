# Generated by Django 3.2.4 on 2021-07-21 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210721_1328'),
        ('rentals', '0007_auto_20210721_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
            ],
            bases=('products.product',),
        ),
    ]
