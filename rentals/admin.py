from django.contrib import admin

from .models import RentalFulfilment, RentalPriceAdjustment

# Register your models here.
admin.site.register(RentalFulfilment)
admin.site.register(RentalPriceAdjustment)