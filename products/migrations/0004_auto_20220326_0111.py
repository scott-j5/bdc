# Generated by Django 3.2.4 on 2022-03-26 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_base_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productfulfilment',
            old_name='fulfilled_price',
            new_name='_fulfilment_price',
        ),
        migrations.RenameField(
            model_name='productfulfilment',
            old_name='fulfilled_product_price',
            new_name='audit_product_base_price',
        ),
    ]
