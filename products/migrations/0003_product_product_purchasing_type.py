# Generated by Django 3.2.4 on 2021-07-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_sale_productpriceadjustment_deal'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_purchasing_type',
            field=models.CharField(choices=[('RENTAL', 'Rental'), ('OUTRIGHT', 'Outright')], default='OUTRIGHT', max_length=10),
        ),
    ]