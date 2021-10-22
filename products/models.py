import math
import random

from core.models import get_sentinel_user
from core.utils import get_sentinel_date, daterange
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone
from imageit.models import ScaleItImageField
from invoicing.models import PriceAdjustment

# Create your models here.
def get_sentinel_product():
    return Product.objects.get_or_create(name='deleted')[0]

def get_sentinel_price_adjustment():
    return PriceAdjustment.objects.get_or_create(name='deleted', period_start=get_sentinel_date, period_end=get_sentinel_date)[0]


class ProductFeature(models.Model):
	name = models.CharField(max_length=200, blank=False, null=False, unique=True)
	description = models.TextField(blank=True, null=False)
	icon_class = models.CharField(max_length=100, blank=True, null=False, help_text='Search Bootstrap icons, Feather Icons or Font awesome icons for available class names.')

	def __str__(self):
		return f'{self.name}'

class Product(models.Model):
	slug = models.SlugField(blank=True, null=False, unique=True, help_text="Url appropriate characters only, no spaces")
	name = models.CharField(max_length=50, blank=False, null=False, unique=True)
	description_short = models.TextField(null=True, blank=True)
	description_long = models.TextField(null=True, blank=True)
	rentable = models.BooleanField(default=False)
	base_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="On rentable items, rates are calculated and charged hourly!")
	available = models.BooleanField(default=False)
	qty = models.IntegerField(default=0)
	features = models.ManyToManyField(ProductFeature)

	def __str__(self):
		return self.name

	@property
	def primary_img(self):
		imgs = self.productimage_set.filter(primary=True)
		if imgs.count() > 0:
			idx = random.randint(0, imgs.count() - 1)
			return imgs[idx]
		else:
			imgs = self.productimage_set.filter()
			if imgs.count() > 0:
				idx = random.randint(0, imgs.count() - 1)
				return imgs[idx]
			return imgs

	@property
	def banner(self):
		banners = self.productimage_set.filter(banner=True)
		if banners.count() > 0:
			idx = random.randint(0, banners.count() - 1)
			return banners[idx]
		else:
			imgs = self.productimage_set.filter()
			if imgs.count() > 0:
				idx = random.randint(0, imgs.count() - 1)
				return imgs[idx]
			return imgs

	@property
	def thumbnail(self):
		thumbs = self.productimage_set.filter(thumbnail=True)
		if thumbs.count() > 0:
			idx = random.randint(0, thumbs.count() - 1)
			return thumbs[idx]
		else:
			imgs = self.productimage_set.filter()
			if imgs.count() > 0:
				idx = random.randint(0, imgs.count() - 1)
				return imgs[idx]
			return imgs

	def clean(self):
		self.slug = self.name.replace(' ', '-').lower()
		if self.qty <= 0:
			self.available = False


class ProductImage(models.Model):
	def get_upload_path(instance, filename):
		return f"product_images/{instance.product.slug}/{filename}"

	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = ScaleItImageField(max_width=1500, max_height=1500, quality=100, upload_to=get_upload_path)
	primary = models.BooleanField(default=False, help_text="Square shape reccomended. Primary images should really highlight the essence of the product")
	banner = models.BooleanField(default=False, help_text="Banner images should be in a landscape format for best results")
	thumbnail = models.BooleanField(default=False, help_text="Thumbnail photo dimensions should be square for best results")

	def __str__(self):
		return f"{self.product.name} - {self.image.name}"


class ProductFulfilment(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET(get_sentinel_product))
	fulfilment_date_time = models.DateTimeField(default=timezone.now)
	fulfilled_product_base_price = models.DecimalField(null=False, blank=True, max_digits=10, decimal_places=2)
	fulfilled_price = models.DecimalField(null=False, blank=True, max_digits=10, decimal_places=2)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not kwargs.get('fulfilment_date_time'):
			self.fulfilment_date_time = timezone.now()

	def __str__(self):
		return f"{ self.product.name } - (${ self.fulfilled_price }) { self.fulfilment_date_time }"

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

	def save(self, *args, **kwargs):
		if not self.fulfilled_product_base_price:
			self.fulfilled_product_base_price = self.product.base_price
		self.fulfilled_price = self.fulfilment_price
		# Add info about adjustments here? fk to adj?
		return super().save(*args, **kwargs)


class ProductPriceAdjustment(PriceAdjustment):
	products = models.ManyToManyField(Product, blank=True)
	deal = models.BooleanField(default=False)