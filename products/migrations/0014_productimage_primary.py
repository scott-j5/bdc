# Generated by Django 3.2.4 on 2021-10-22 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_productfeature_icon_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='primary',
            field=models.BooleanField(default=False, help_text='Square shape reccomended. Primary images should really highlight the essence of the product'),
        ),
    ]