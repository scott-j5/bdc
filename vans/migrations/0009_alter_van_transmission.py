# Generated by Django 3.2.4 on 2022-03-05 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vans', '0008_van_transmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='van',
            name='transmission',
            field=models.CharField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')], max_length=10),
        ),
    ]
