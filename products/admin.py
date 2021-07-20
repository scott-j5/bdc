from django.contrib import admin

from .models import Product, ProductPriceAdjustment

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductPriceAdjustment)