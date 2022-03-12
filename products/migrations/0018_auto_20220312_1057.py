# Generated by Django 3.2.4 on 2022-03-12 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20220312_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfulfilment',
            name='price_override',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Override default pricing', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='productfulfilment',
            name='fulfilled_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Records actual fulfilled price', max_digits=10),
        ),
        migrations.AlterField(
            model_name='productfulfilment',
            name='fulfilled_product_base_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Records the product base price at time of fulfilment', max_digits=10),
        ),
    ]
