# Generated by Django 3.2.4 on 2022-04-22 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0013_auto_20220422_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentaldriver',
            name='licence_check_code',
            field=models.CharField(blank=True, help_text='Click <a href="https://www.gov.uk/view-driving-licence" target="_blank"><u>HERE</u></a> for more information', max_length=20, null=True, verbose_name='DVLA Check code'),
        ),
    ]