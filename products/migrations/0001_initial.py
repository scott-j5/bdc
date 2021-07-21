# Generated by Django 3.2.4 on 2021-07-20 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoicing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=50)),
                ('description_short', models.TextField(blank=True, null=True)),
                ('description_long', models.TextField(blank=True, null=True)),
                ('rentable', models.BooleanField(default=False)),
                ('base_price', models.IntegerField(default=0, help_text='On rentable items, rates are calculated and charged hourly!')),
                ('available', models.BooleanField(default=False)),
                ('qty', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductPriceAdjustment',
            fields=[
                ('priceadjustment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='invoicing.priceadjustment')),
                ('sale', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(blank=True, to='products.Product')),
            ],
            bases=('invoicing.priceadjustment',),
        ),
    ]
