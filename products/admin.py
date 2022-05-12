from django.contrib import admin

from .models import (
	Product,
	ProductFeature,
	ProductFulfilment,
	ProductImage,
	ProductPriceAdjustment,
	Review
	)

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductFeature)
admin.site.register(ProductFulfilment)
admin.site.register(ProductImage)
admin.site.register(ProductPriceAdjustment)
admin.site.register(Review)