# Generated by Django 3.2.4 on 2021-10-22 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20211022_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeature',
            name='icon_class',
            field=models.CharField(blank=True, help_text='Bootstrap icons, Feather Icons and Font awesome icon class names may be used. Google search those providers for available icons.', max_length=100),
        ),
    ]