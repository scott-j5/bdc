import math
import random
import datetime

from core.models import get_sentinel_user
from core.utils import get_sentinel_date, daterange, format_price
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone
from imageit.models import ScaleItImageField
from invoicing.models import PriceAdjustment

from rentals.settings import CHARGE_RENTAL_DAILY, VERBOSE_CHARGE_PERIOD

# Create your models here.
def get_sentinel_product():
    return Product.objects.get_or_create(name='deleted')[0]

def get_sentinel_price_adjustment():
    return PriceAdjustment.objects.get_or_create(name='deleted', period_start=get_sentinel_date, period_end=get_sentinel_date)[0]


class ProductFeature(models.Model):
	name = models.CharField(max_length=200, blank=False, null=False, unique=True)
	slug = models.SlugField(unique=True, blank=True, null=False)
	description = models.TextField(blank=True, null=False)
	icon_class = models.CharField(max_length=100, blank=True, null=False, help_text='Search Bootstrap icons, Feather Icons or Font awesome icons for available class names.')

	def __str__(self):
		return f'{self.name}'

	def clean(self, *args, **kwargs):
		if self.slug == '' or self.slug == None:
			self.slug = self.name.replace(' ', '-').lower()
		super().clean(*args, **kwargs)	


class Product(models.Model):
	slug = models.SlugField(unique=True, blank=True, null=False, help_text="Url appropriate characters only, no spaces")
	name = models.CharField(max_length=50, blank=False, null=False, unique=True)
	description_short = models.TextField(null=True, blank=True)
	description_long = models.TextField(null=True, blank=True)
	base_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Price", help_text=f"On Rentable items price is the equivelant { VERBOSE_CHARGE_PERIOD } rate before adjustments!")
	qty = models.IntegerField(default=0)
	features = models.ManyToManyField(ProductFeature, blank=True)
	available = models.BooleanField(default=False)

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
		if self.slug == '' or self.slug == None:
			self.slug = self.name.replace(' ', '-').lower()
		if self.qty <= 0:
			self.available = False
		super().clean()
	
	@staticmethod
	def get_price_help_text():
		return f"Base price before adjustments are made."


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


class ProductFulfilmentManager(models.Manager):
	def instantiate_fulfilment(self, product, fulfilling_user=None, fulfilment_date_time=timezone.now()):
		if isinstance(fulfilment_date_time, datetime.date):
			if timezone.is_naive(fulfilment_date_time):
				self.fulfilment_date_time = timezone.make_aware(fulfilment_date_time)
			else:
				self.fulfilment_date_time = fulfilment_date_time
		else:
			self.fulfilment_date_time = timezone.make_aware(datetime.datetime.strptime(kwargs.get('fulfilment_date_time'), '%Y-%m-%d'))
		return ProductFulfilment(product=product, fulfilling_user=fulfilling_user, fulfilment_date_time=fulfilment_date_time)

	def create_fulfilment(self, product, fulfilling_user=None, fulfilment_date_time=timezone.now()):
		obj = self.instantiate_fulfilment(product, fulfilling_user, fulfilment_date_time)
		obj.full_clean()
		obj.save()
		return obj


class ProductFulfilment(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET(get_sentinel_product))
	audit_product_base_price = models.DecimalField(null=False, blank=True, max_digits=10, decimal_places=2, help_text="Records the product base price at time of fulfilment")
	fulfilling_user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), blank=False, null=False)
	fulfilment_date_time = models.DateTimeField(default=timezone.now)
	_fulfilment_price = models.DecimalField(null=False, blank=True, max_digits=10, decimal_places=2, help_text="Records actual fulfilled price")
	price_override = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, help_text="Override default pricing")

	objects = ProductFulfilmentManager()

	def __str__(self):
		return f"{ self.product.name } - ({ format_price(self._fulfilment_price) }) { self.fulfilment_date_time }"

	@property
	def fulfilment_price(self):
		return self._calculate_price()
		#return self._fulfilment_price if self._fulfilment_price else self._calculate_price()

	def _calculate_price(self):
		if hasattr(self, '_calculated_price'):
			return self._calculated_price
		else:
			if self.price_override is not None:
				self.fulfilment_price = self.price_override
			else:
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
			self._calculated_price = round(fulfilment_price, 2)
			return self._calculated_price

	@property
	def active_price_adjustments(self):
		#include logic
		return self.product.productpriceadjustment_set.filter(period_start__lte=self.fulfilment_date_time, period_end__gte=self.fulfilment_date_time)

	@property
	def active_deals(self):
		return self.product.productpriceadjustment_set.filter(period_start__lte=self.fulfilment_date_time, period_end__gte=self.fulfilment_date_time, display_to_user=True)

	def save(self, *args, **kwargs):
		if not self.audit_product_base_price:
			self.audit_product_base_price = self.product.base_price
		self._fulfilment_price = self._calculate_price()
		# Add info about adjustments here? fk to adj?
		return super().save(*args, **kwargs)


class ProductPriceAdjustment(PriceAdjustment):
	products = models.ManyToManyField(Product, blank=True)
	display_to_user = models.BooleanField(default=False)