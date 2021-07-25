from datetime import datetime
import json
import math

from core.models import get_sentinel_user
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from invoicing.models import PriceAdjustment
from products.models import Product, ProductFulfilment, get_sentinel_product
from core.utils import datediff_hours, get_date_overlap

# Create your models here.
class RentalProductManager(models.Manager):
	def get_query_set(self):
		return self.filter(is_rentable=True).exclude(slug="deleted")


class RentalProduct(Product):
	objects = RentalProductManager()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qty = 1;

	# Returns a list of dates where the product is unavailable
	## Not configured for HOURLY RENTALS AS FLATPICKR HAS NO MEANS TO DO SO
	@property
	def unavailable(self):
		return RentalFulfilment.objects.filter(rental_fulfilled_product__product=self).values_list('rental_start', 'rental_end')
	
	# Returns a flatpickr compliant list of unavailable date ranges
	@property
	def flatpickr_unavailable(self):
		formatted_dates = []
		for start_date, end_date in self.unavailable:
			date_range = {
				"from": datetime.strftime(start_date, '%Y-%m-%d'),
				"to": datetime.strftime(end_date, '%Y-%m-%d'),
			}
			formatted_dates.append(date_range)
		return formatted_dates

	def is_available(self, dt_range):
		# Select Rental Fulfilments where rental start or rental end are within the specified range or that end after range start or begin before range end
		clashing_rentals = RentalFulfilment.objects.filter(
			Q(rental_start__range=(dt_range[0], dt_range[1]))
			| Q(rental_end__range=(dt_range[0], dt_range[1]))
			| Q(rental_start__lte=dt_range[0], rental_end__gte=dt_range[1])
		)
		return False if len(clashing_rentals) > 0 else True

	@staticmethod
	def get_available(dt_range):
		# Exclude Rental Fulfilments where rental start or rental end are within the specified range or that end after range start or begin before range end
		unavailable_products = RentalFulfilment.objects.filter(
			Q(rental_start__range=(dt_range[0], dt_range[1]))
			| Q(rental_end__range=(dt_range[0], dt_range[1]))
			| Q(rental_start__lte=dt_range[0], rental_end__gte=dt_range[1])
		).values_list('product__id', flat=True)
		return RentalProduct.objects.exclude(id__in=unavailable_products)

	class Meta:
		proxy = True


class RentalFulfilment(ProductFulfilment):
	rental_fulfilled_product = models.ForeignKey(ProductFulfilment, on_delete=models.SET(get_sentinel_product), related_name='fulfilled_product')
	rental_start = models.DateTimeField(blank=False, null=False)
	rental_end = models.DateTimeField(blank=False, null=False)
	rental_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fulfilment_date = timezone.make_aware(datetime.datetime.strptime(kwargs.get('fulfilment_date'), '%Y-%m-%d')) if kwargs.get('fulfilment_date') else timezone.now()
		# If a product (not fulfilment) is specified a product fulfilment is created automatically
		if kwargs.get("product"):
			self.rental_fulfilled_product = ProductFulfilment(product=kwargs.get("product"), fulfilment_date_time=self.fulfilment_date_time)
		if kwargs.get("rental_fulfilled_product"):
			self.product = kwargs.get("rental_fulfilled_product").product
		if hasattr(self, 'rental_fulfilled_product'):
			self.rental_price = self._calculate_price()
			self.fulfilled_product_base_price = (self.rental_fulfilled_product.fulfilment_price * self.duration_hours)

	@property
	def active_price_adjustments(self):
		# Select adjustments where start date or end date is within rental period or that begin before rental and end after rental
		price_adjustments = self.rental_fulfilled_product.product.rentalpriceadjustment_set.filter(
			Q(period_start__range=(self.rental_start, self.rental_end))
			| Q(period_end__range=(self.rental_start, self.rental_end))
			| Q(period_start__lte=self.rental_start, period_end__gte=self.rental_end)
		)
		return price_adjustments

	@property
	def clashing_rentals(self):
		# Select Rental Fulfilments where rental start or rental end are within an existing rental period or that end after self.rental start or begin before self.rental end
		return RentalFulfilment.objects.filter(
			Q(rental_start__range=(self.rental_start, self.rental_end))
			| Q(rental_end__range=(self.rental_start, self.rental_end))
			| Q(rental_start__lte=self.rental_start, rental_end__gte=self.rental_end)
		)

	@property
	def duration_hours(self):
		delta = self.rental_end - self.rental_start
		return datediff_hours(delta)

	@property
	def duration(self):
		diff = self.rental_end - self.rental_start
		days, seconds = diff.days, diff.seconds
		if days >= .5:
			pluralize = "s" if days > 1 else ""
			return f"{math.ceil(days)} Day{pluralize}"
		else:
			hours = math.ceil(days * 24 + seconds // 3600)
			pluralize = "s" if hours > 1 else ""
			return f"{hours} Hour{pluralize}"

	@property
	def fulfilment_price(self):
		return self.rental_price if self.rental_price else self._calculate_price()

	@property
	def product_available(self):
		return self.product.rentalproduct.is_available([self.rental_start, self.rental_end])

	#Calculates the total price of a reservation based on all applicable price adjustments
	def _calculate_price(self):
		product_fulfilment_price = self.rental_fulfilled_product.fulfilment_price
		total_price = product_fulfilment_price * self.duration_hours
		adjustment_val = 0
		
		for adj in self.active_price_adjustments:
				applicable_range = datediff_hours(get_date_overlap([adj.period_start, adj.period_end], [self.rental_start, self.rental_end]))
				# take the hourly fulfilment price and Apply Additions and deductions to total price
				# based on the time period with which the price adjustment applies
				if adj.adj_type == 'PER':
					adjustment_val = adjustment_val + (((product_fulfilment_price * adj.adj_amount) / 100) * applicable_range)
				elif adj.adj_type == 'DOL':
					adjustment_val = adjustment_val + (adj.adj_amount * applicable_range)

			#Find length valid within rental (hours)
			#Derive pricing alteration from fulfilment_price * hours
			#Adjust total price accordingly
			#Take deductions from added
		
		return round(total_price + adjustment_val, 2)
	
	def clean(self, *args, **kwargs):
		# Need to impliment check for overlapping rentals Including buffer
		return super().clean(*args, **kwargs)

	def save(self, *args, **kwargs):
		if not self.fulfilled_product_base_price:
			self.fulfilled_product_base_price = (self.rental_fulfilled_product.fulfilment_price * self.duration_hours)
		if not self.rental_price:
			self.rental_price = self._calculate_price()
		return super().save(*args, **kwargs)


class RentalPriceAdjustment(PriceAdjustment):
	products = models.ManyToManyField(Product)