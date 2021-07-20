import math

from core.models import get_sentinel_user
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from invoicing.models import PriceAdjustment
from products.models import Product, get_sentinel_product
from core.utils import datediff_hours, get_date_overlap

# Create your models here.
class Reservation(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
	check_in = models.DateTimeField()
	check_out = models.DateTimeField()

	def length_days(self):
		return abs((self.check_out - self.check_in).days)


class ProductRental(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
	product = models.ForeignKey(Product, on_delete=models.SET(get_sentinel_product))
	rental_start = models.DateTimeField(blank=False, null=False)
	rental_end = models.DateTimeField(blank=False, null=False)
	rental_price = models.IntegerField()

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

	#Calculates the total price of a reservation based on all applicable price adjustments
	@property
	def total_price(self):
		fulfilment_price = self.product.fulfilment_price
		total_price = fulfilment_price * self.duration_hours
		adjustment_val = 0
		
		# Select adjustments where start date or end date is within rental period or that begin before rental and end after rental
		price_adjustments = self.product.rentalpriceadjustment_set.filter(
			Q(period_start__range=(self.rental_start, self.rental_end))
			| Q(period_end__range=(self.rental_start, self.rental_end))
			| Q(period_start__lte=self.rental_start, period_end__gte=self.rental_end)
		)
		
		for adj in price_adjustments:
				applicable_range = datediff_hours(get_date_overlap([adj.period_start, adj.period_end], [self.rental_start, self.rental_end]))
				# take the hourly fulfilment price and Apply Additions and deductions to total price
				# based on the time period with which the price adjustment applies
				if adj.adj_type == 'PER':
					adjustment_val = adjustment_val + (((fulfilment_price * adj.adj_amount) / 100) * applicable_range)
				elif adj.adj_type == 'DOL':
					adjustment_val = adjustment_val + (adj.adj_amount * applicable_range)

			#Find length valid within rental (hours)
			#Derive pricing alteration from fulfilment_price * hours
			#Adjust total price accordingly
			#Take deductions from added
		
		return total_price + adjustment_val


class RentalPriceAdjustment(PriceAdjustment):
	rentals = models.ManyToManyField(Product)