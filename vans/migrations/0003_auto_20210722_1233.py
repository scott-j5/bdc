# Generated by Django 3.2.4 on 2021-07-22 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210721_1328'),
        ('vans', '0002_auto_20210721_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='van',
            name='rentalproduct_ptr',
        ),
        migrations.AddField(
            model_name='van',
            name='product_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product'),
            preserve_default=False,
        ),
    ]
