# Generated by Django 3.2.4 on 2022-04-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceadjustment',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
