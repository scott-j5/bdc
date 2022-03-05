# Generated by Django 3.2.4 on 2022-03-05 09:21

import core.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rentals', '0012_rentalinformation_rentalrules'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalfulfilment',
            name='rental_user',
            field=models.ForeignKey(default=1, on_delete=models.SET(core.models.get_sentinel_user), to='auth.user'),
            preserve_default=False,
        ),
    ]
