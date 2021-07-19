import math

from core.models import get_sentinel_user
from django.db import models
from django.contrib.auth.models import User
from products.models import Product, get_sentinel_product

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

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rental_price = self.calculate_price()

	def duration_hours(self):
		diff = self.rental_end - self.rental_start
		days, seconds = diff.days, diff.seconds
		return days * 24 + seconds // 3600

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
	def calculate_price(self):
		total_price = self.product.fulfilment_price * self.duration_hours()
		'''
		# Select adjustments where start date or end date is within rental period
		adjustments = self.product.price_adjustment_set.filter(
			Q(period_start__range=(self.reservation_start, self.reservation_end)) 
			| Q(period_end__range=(self.reservation_start, self.reservation_end))
		)
		
		#Loop over days of the reservation, calculating the daily rate for each
		for day in daterange(self.reservation_start.date(), self.reservation_end.date())
			# Select adjustments applicable to this particular day
			daily_adjustments = adjustments.filter(period_start__lte=day, period_end__gte=day)

			#Loop over adjustments here (maybe return as a list to reducr db calls?
			#Apply Additions

			#Apply Deductions
		'''
		return total_price