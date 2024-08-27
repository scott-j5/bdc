# Generated by Django 3.2.13 on 2022-05-02 11:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productfulfilment_updated_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField()),
                ('product_fulfillment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productfulfilment')),
            ],
        ),
    ]