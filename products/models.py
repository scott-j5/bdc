import math

from core.models import get_sentinel_user
from core.utils import get_sentinel_date, daterange
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone


# Create your models here.
def get_sentinel_product():
    return Product.objects.get_or_create(name='deleted')[0]

def get_sentinel_price_adjustment():
    return PriceAdjustment.objects.get_or_create(name='deleted', period_start=get_sentinel_date, period_end=get_sentinel_date)[0]


class Product(models.Model):
	slug = models.SlugField(blank=True, null=False)
	name = models.CharField(max_length=50, blank=False, null=False)
	description_short = models.TextField(null=True, blank=True)
	description_long = models.TextField(null=True, blank=True)
	rentable = models.BooleanField(default=False)
	base_price = models.IntegerField(default=0, help_text="On rentable items, rates are calculated and charged hourly!")
	available = models.BooleanField(default=False)
	qty = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def clean(self):
		self.slug = self.name.replace(' ', '-').lower()
		if self.qty <= 0:
			self.available = False
	
	@property
	def fulfilment_price(self):
		fulfilment_price = self.base_price
		price_adjustments = self.priceadjustment_set.filter(period_start__lte=timezone.now(), period_end__gte=timezone.now())
		for adj in price_adjustments:
			#Apply Additions (additions are non-compounding)
			if adj.adj_amount > 0:
				if adj.adj_type == 'PER':
					fulfilment_price = fulfilment_price + ((self.base_price * adj.adj_amount) / 100)
				elif adj.adj_type == 'DOL':
					fulfilment_price = fulfilment_price + adj.adj_amount

		for adj in price_adjustments:
			#Apply Deductions (deductions are negatively compounding)
			if adj.adj_amount < 0:
				if adj.adj_type == 'PER':
					fulfilment_price = fulfilment_price - ((fulfilment_price * adj.adj_amount) / 100)
				elif adj.adj_type == 'DOL':
					fulfilment_price = fulfilment_price - adj.adj_amount
		return fulfilment_price


class PriceAdjustment(models.Model):
	ADJ_TYPES = [('PER', '%'), ('DOL', '$')]
	slug = models.SlugField(blank=True, null=False)
	name = models.CharField(max_length=50, blank=False, null=False)
	products = models.ManyToManyField(Product)
	description = models.TextField()
	period_start = models.DateTimeField(blank=False, null=False)
	period_end = models.DateTimeField(blank=False, null=False)
	adj_type = models.CharField(max_length=3, choices=ADJ_TYPES, default='PER', blank=False, null=False)
	adj_amount = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return f"{self.name} {self.start}-{self.end}({self.adj_amount}{self.adj_type})"

	def clean(self):
		if not self.slug or self.slug == '':
			self.slug = self.name.replace(' ', '-').lower()