import math

from core.models import get_sentinel_user
from core.utils import get_sentinel_date, daterange
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone
from invoicing.models import PriceAdjustment

# Create your models here.
def get_sentinel_product():
    return Product.objects.get_or_create(name='deleted')[0]

def get_sentinel_price_adjustment():
    return PriceAdjustment.objects.get_or_create(name='deleted', period_start=get_sentinel_date, period_end=get_sentinel_date)[0]


class Product(models.Model):
	slug = models.SlugField(blank=True, null=False, unique=True)
	name = models.CharField(max_length=50, blank=False, null=False, unique=True)
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
	
	# Returns an array of unavailable days from today in format 'yyyy-mm-dd'
	@property
	def unavailable(self):
		return []


class ProductFulfilment(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET(get_sentinel_product))
	product_base_price = models.IntegerField(null=False)
	fulfilment_date_time = models.DateTimeField(default=timezone.now)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not kwargs.get('fulfilment_date_time'):
			self.fulfilment_date_time = timezone.now()
		self.product_base_price = self.product.base_price

	@property
	def fulfilment_price(self):
		fulfilment_price = self.product.base_price
		for adj in self.active_price_adjustments:
			#Apply Additions (additions are non-compounding)
			if adj.adj_amount > 0:
				if adj.adj_type == 'PER':
					fulfilment_price = fulfilment_price + ((self.product.base_price * adj.adj_amount) / 100)
				elif adj.adj_type == 'DOL':
					fulfilment_price = fulfilment_price + adj.adj_amount

		for adj in self.active_price_adjustments:
			#Apply Deductions (deductions are negatively compounding)
			if adj.adj_amount < 0:
				if adj.adj_type == 'PER':
					fulfilment_price = fulfilment_price + ((fulfilment_price * adj.adj_amount) / 100)
				elif adj.adj_type == 'DOL':
					fulfilment_price = fulfilment_price + adj.adj_amount
		return round(fulfilment_price, 2)

	@property
	def active_price_adjustments(self):
		return self.product.productpriceadjustment_set.filter(period_start__lte=self.fulfilment_date_time, period_end__gte=self.fulfilment_date_time)

	@property
	def active_deals(self):
		return self.product.productpriceadjustment_set.filter(period_start__lte=self.fulfilment_date_time, period_end__gte=self.fulfilment_date_time, deal=True)


class ProductPriceAdjustment(PriceAdjustment):
	products = models.ManyToManyField(Product, blank=True)
	deal = models.BooleanField(default=False)