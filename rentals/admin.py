from django.contrib import admin

from .models import RentalInformation, RentalFulfilment, RentalPriceAdjustment, RentalRules

# Register your models here.
admin.site.register(RentalInformation)
admin.site.register(RentalFulfilment)
admin.site.register(RentalPriceAdjustment)
admin.site.register(RentalRules)