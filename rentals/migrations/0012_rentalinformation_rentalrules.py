# Generated by Django 3.2.4 on 2021-10-26 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0011_alter_rentalfulfilment_rental_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RentalRules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
