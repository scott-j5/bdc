# Generated by Django 3.2.4 on 2022-03-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vans', '0007_alter_van_drive_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='van',
            name='transmission',
            field=models.CharField(choices=[('MT', 'Manual'), ('AT', 'Automatic')], default='MT', max_length=2),
            preserve_default=False,
        ),
    ]
