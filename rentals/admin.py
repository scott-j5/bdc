from django.contrib import admin

from .models import (
	RentalExtra,
	Rental,
	RentalInformation,
	RentalPriceAdjustment,
	RentalRules
)

# Register your models here.
admin.site.register(RentalExtra)
admin.site.register(Rental)
admin.site.register(RentalInformation)
admin.site.register(RentalPriceAdjustment)
admin.site.register(RentalRules)