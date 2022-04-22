# Generated by Django 3.2.4 on 2022-04-21 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0011_rentaldriver_proof_of_address_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentaldriver',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rentaldriver',
            name='status',
            field=models.CharField(choices=[('APP', 'Approved'), ('ARV', 'Awaiting Review'), ('ARQ', 'Action Required'), ('DND', 'Denied')], default='ARV', max_length=3),
        ),
    ]
