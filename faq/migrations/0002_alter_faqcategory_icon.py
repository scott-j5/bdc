# Generated by Django 3.2.13 on 2022-05-02 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqcategory',
            name='icon',
            field=models.CharField(help_text="Available icon classes are available <a href='https://fontawesome.com/search?m=free'><u>HERE</u></a>", max_length=150),
        ),
    ]