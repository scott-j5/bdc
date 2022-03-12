from django.contrib import admin

from .models import (
	RentalExtra,
	RentalFulfilment,
	RentalInformation,
	RentalPriceAdjustment,
	RentalRules
)

# Register your models here.
admin.site.register(RentalExtra)
admin.site.register(RentalFulfilment)
admin.site.register(RentalInformation)
admin.site.register(RentalPriceAdjustment)
admin.site.register(RentalRules)