# Generated by Django 3.2.4 on 2022-03-01 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_alter_tag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default=1, max_length=100),
        ),
    ]