from datetime import datetime, timedelta
import json
import math

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from imageit.models import ScaleItImageField, CropItImageField
from mapbox_location_field.models import LocationField, AddressAutoHiddenField

from core.models import get_sentinel_user
from core.templatetags.price_tags import price
from core.utils import parse_date_range_day_inclusive, datediff_days, datediff_hours, get_date_overlap,format_price
from invoicing.models import PriceAdjustment
from products.models import Product, ProductFulfilment, ProductFulfilmentManager, get_sentinel_product

from .settings import CHARGE_RENTAL_DAILY, RENTAL_CHECK_IN_TIME

# Create your models here.
class RentalProductManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(rentable=True).exclude(slug="deleted")

	# Return all rental products available within a date range
	# rental_start, rental_end: datetime
	def available(self, rental_start, rental_end):
		qs = self.get_queryset()
		unavailable_products = RentalFulfilment.objects.filter(
			Q(rental_start__range=(rental_start, rental_end))
			| Q(rental_end__range=(rental_start, rental_end))
			| Q(rental_start__lte=rental_start, rental_end__gte=rental_end)
		).values_list('product__id', flat=True)
		return qs.exclude(id__in=unavailable_products)

	# Return all rental products available within a 'period' of a defined date range
	# rental_start, rental_end: datetime
	def nearby(self, rental_start, rental_end, days=30):
		# Number of days either side of dt_range to search
		search_period = timedelta(days)
		# Desired length of rental
		length = abs(rental_end - rental_start)
		available_ids = []
		qs = self.get_queryset()
		for rental_product in qs:
			available = rental_product.available_dates
			for period in available:
				# Add rentals of same length, but within search period to available_ids
				if ((period["start"] > timezone.now() or period["end"] - length > timezone.now())
				and (abs(period['start'] - rental_start) < search_period)
				and (abs(period['start'] - period['end']) > length)):
					available_ids.append(rental_product.id)
		return qs.filter(id__in=available_ids)


class RentalProduct(Product):
	rentable = models.BooleanField(null=False, default=True)
	min_turnaround = models.IntegerField(default=1, blank=True, null=True, help_text="Minimum time between return and re-rental in Hours")
	objects = RentalProductManager()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qty = 1

	# Returns a list of datetimes where the rental product is available
	# Returns list of dicts: [{"start": dt, "end", dt},{"start": dt, "end", dt}]
	@property
	def available_dates(self):
		available = []
		unavailable = self.unavailable_dates.order_by('rental_start')
		available_start = timezone.make_aware(datetime.strptime('1111-01-01', '%Y-%m-%d'))
		for unavailable_start, unavailable_end in unavailable:
			# Check for overlap between the start of current unavailable period and next available_period_start
			# If available_period starts after next unavailable_period_start then dont append available range 
			# Change to <= to make include same ending and starting time as available
			if available_start < unavailable_start:
				available_range = {"start": available_start, "end": unavailable_start}
				available.append(available_range)
			available_start = unavailable_end
		available.append({"start": available_start, "end": timezone.make_aware(datetime.strptime('9998-12-31', '%Y-%m-%d'))})
		return available

	# Returns a list of datetimes where the rental product is unavailable
	# Takes into account min_turnaround
	# [{"rental_start": dt, "rental_end", dt},{"rental_start": dt, "rental_end", dt}]
	@property
	def unavailable_dates(self):
		unavailable = RentalFulfilment.objects.filter(product=self).values_list('rental_start', '_rental_end_inc_turnaround')
		return unavailable
	
	# Returns a flatpickr compliant list of unavailable date ranges
	## Not configured for HOURLY RENTALS AS FLATPICKR HAS NO MEANS TO DO SO
	@property
	def flatpickr_unavailable(self):
		formatted_dates = []
		for start_date, end_date in self.unavailable_dates:
			# Check if rental_end is before settings.check-in time. Then set day to available
			if end_date.time() < RENTAL_CHECK_IN_TIME:
				end_date = end_date - timedelta(days=1)
			date_range = {
				"from": datetime.strftime(start_date, '%Y-%m-%d'),
				"to": datetime.strftime(end_date, '%Y-%m-%d'),
			}
			formatted_dates.append(date_range)
		return formatted_dates

	# Return bool if rental_product is available for dt_range
	# rental_start, rental_end: datetime
	def is_available(self, rental_start, rental_end):
		end_inc_turnaround = rental_end + timedelta(hours=self.min_turnaround)

		# Select Rental Fulfilments rental start or rental end are within the specified range
		# or that end after range start or begin before range end
		# Rental fulfil where start > rental_end_inc_turnaround or end < rental_start
		clashing_rentals = RentalFulfilment.objects.filter(
			Q(rental_start__range=(rental_start, end_inc_turnaround))
			| Q(_rental_end_inc_turnaround__range=(rental_start, end_inc_turnaround))
			| Q(rental_start__lte=rental_start, _rental_end_inc_turnaround__gt=end_inc_turnaround)
		).count()
		return False if clashing_rentals > 0 else True
	
	@staticmethod
	def get_price_help_text():
		verbose_charge_period = 'daily' if CHARGE_RENTAL_DAILY else 'hourly'
		return f"Rentable item. This is the equivelant { verbose_charge_period } rate before adjustments!"


class RentalExtra(Product):
	
	def __str__(self):
		return f'{self.name} - {price(self.base_price)}'


class RentalFulfilmentManager(ProductFulfilmentManager):
	def q_from_query_dict(self, query_dict=None):
		fields = [f.name for f in RentalFulfilment._meta.get_fields(include_parents=False)]
		filters = super().q_from_query_dict(query_dict)

		## Generate standard filters from field names
		new_filters = {field_name: value for field_name, value in query_dict.items()
              if value and field_name in fields}
		if query_dict.get('rental_start_range'):
			dates = parse_date_range_day_inclusive(query_dict.get('rental_start_range'))
			new_filters['rental_start__range'] = [dates[0], dates[1]]
		if query_dict.get('rental_end_range'):
			dates = parse_date_range_day_inclusive(query_dict.get('rental_end_range'))
			new_filters['rental_end__range'] = [dates[0], dates[1]]
		filters.update(new_filters)
		return filters if filters is not None else {}

	def query_string_filter(self, query_string=None):
		qs = self.get_queryset().filter(**self.q_from_query_dict(query_string.dict()))
		return qs


class RentalFulfilment(ProductFulfilment):
	class Status(models.TextChoices):
		CONFIRMED = 'CNF', _('Confirmed')
		PENDING = 'PND', _('Pending')
		DENIED = 'DND', _('Denied')
		COMPLETED = 'CMP', _('Completed')

	status = models.CharField(max_length=3, choices=Status.choices, default=Status.PENDING)
	rental_start = models.DateTimeField(blank=False, null=False)
	rental_end = models.DateTimeField(blank=False, null=False)
	_rental_end_inc_turnaround = models.DateTimeField(default=timezone.now, blank=False, null=False)
	_fulfilled_rental_rate = models.DecimalField(blank=True, max_digits=10, decimal_places=2, help_text="Fulfilled rate for rental. (rate after adjustments) to be multiplied by duration")
	_unfulfilled_rental_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2, help_text="Total cost of the rental before applying rental adjustments")
	rental_extras = models.ManyToManyField(RentalExtra, blank=True)
	pickup_location = LocationField(null=True, blank=True, help_text="Leave blank if not required", map_attrs={'center': [-3.188512, 55.953480], 'placeholder': 'Search'})
	pickup_address = AddressAutoHiddenField(null=True, blank=True)

	objects = RentalFulfilmentManager()

	def __str__(self):
		return f"{self.product.name} - {self.duration_humanize} {format_price(self.fulfilment_price)} ({self.rental_start} - {self.rental_end})"

	@property
	def active_rental_price_adjustments(self):
		# Select adjustments where start date or end date is within rental period or that begin before rental and end after rental
		price_adjustments = self.product.rentalproduct.rentalpriceadjustment_set.filter(
			Q(period_start__range=(self.rental_start, self.rental_end))
			| Q(period_end__range=(self.rental_start, self.rental_end))
			| Q(period_start__lte=self.rental_start, period_end__gte=self.rental_end)
		)
		return price_adjustments

	# Find clashing rentals. include product turnaround time
	@property
	def clashing_rentals(self):
		excl_id = self.id if self.id is not None else -1
		# Select Rental Fulfilments where rental start or rental end are within an existing rental period or that end after self.rental start or begin before self.rental end
		return RentalFulfilment.objects.filter(
			Q(product=self.product),
			Q(rental_start__range=(self.rental_start, self.rental_end_inc_turnaround))
			| Q(rental_end__range=(self.rental_start, self.rental_end_inc_turnaround))
			| Q(rental_start__lte=self.rental_start, rental_end__gte=self.rental_end_inc_turnaround)
		).exclude(id=excl_id)

	# Check for clash including product turnaround time
	@property
	def rental_clash(self):
		return True if len(self.clashing_rentals) > 0 else False

	@property
	def rental_end_inc_turnaround(self):
		return self.rental_end + timedelta(hours=self.product.rentalproduct.min_turnaround)

	@property
	def duration_hours(self):
		delta = self.rental_end - self.rental_start
		return datediff_hours(delta)

	@property
	def duration_days(self):
		delta = self.rental_end - self.rental_start
		return math.ceil(datediff_days(delta))

	@property
	def duration_humanize(self):
		if self.duration_hours <= 24 and not CHARGE_RENTAL_DAILY:
			return f"{self.duration_hours} Hour"
		else:
			return f"{self.duration_days} Night"

	@property
	def duration_humanize_plural(self):
		if self.duration_hours <= 24 and not CHARGE_RENTAL_DAILY:
			pluralize = "s" if self.duration_hours > 1 else ""
			return f"{self.duration_hours} Hour{pluralize}"
		else:
			pluralize = "s" if self.duration_days > 1 else ""
			return f"{self.duration_days} Night{pluralize}"

	@property
	def rental_commenced(self):
		if self.rental_start < timezone.now():
			return True
		return False

	@property
	def drivers(self):
		return self.rental_driver_set.all().count()

	# Calculates the rental rate after product price adjustments
	@property
	def fulfilled_rental_rate(self):
		# Call super _calculate_price() to calculate the rental rate
		return super()._calculate_price()

	# Calculates the total rental price with no rental price adjustments applied 
	@property 
	def unfulfilled_rental_price(self):
		if CHARGE_RENTAL_DAILY:
			total_unfulfilled_rental_price = self.fulfilled_rental_rate * self.duration_days
		else:
			total_unfulfilled_rental_price = self.fulfilled_rental_rate * self.duration_hours
		return total_unfulfilled_rental_price
	
	@property
	def fulfilled_rental_price(self):
		base_rental_price = self.unfulfilled_rental_price
		adjustment_val = 0
		
		for adj in self.active_rental_price_adjustments:
			if CHARGE_RENTAL_DAILY:
				applicable_range = math.ceil(datediff_days(get_date_overlap([adj.period_start, adj.period_end], [self.rental_start, self.rental_end])))
			else:
				applicable_range = datediff_hours(get_date_overlap([adj.period_start, adj.period_end], [self.rental_start, self.rental_end]))
				
			# Take the hourly or daily fulfilment price and Apply Additions and deductions to total price
			# Based on the time period with which the price adjustment applies
			if adj.adj_type == 'PER':
				adjustment_val = adjustment_val + (((self.fulfilled_rental_rate * adj.adj_amount) / 100) * applicable_range)
			elif adj.adj_type == 'DOL':
				adjustment_val = adjustment_val + (adj.adj_amount * applicable_range)

			#Find length valid within rental
			#Derive pricing alteration from fulfilment_price * hours
			#Adjust total price accordingly
			#Take deductions from additions
		
		return round(base_rental_price + adjustment_val, 2)

	@property
	def status_class(self):
		return {
			self.Status.CONFIRMED: 'success',
			self.Status.PENDING: 'info',
			self.Status.DENIED: 'danger',
			self.Status.COMPLETED: 'success',
		}.get(self.status, 'info')

	# Calculates final fulfilment price of the rental
	# Applies RentalPriceAdjustments to unfulfilled_rental_price
	def _calculate_price(self):
		if hasattr(self, '_calculated_rental_price'):
			return self._calculated_rental_price
		else:
			rental_price = self.fulfilled_rental_price
			adjustment_val = 0
			
			# Add the price of any extras
			# Don't apply to non-db objects bc they will have no many to many relation
			if self.id is not None:
				extras = self.rental_extras.all()
				for extra in extras:
					adjustment_val = adjustment_val + extra.base_price

				# Add the price of additional drivers
				drivers_count = max(self.rentaldriver_set.all().count() - 1, 0)
				adjustment_val = adjustment_val + (25 * drivers_count)
			
			self._calculated_rental_price = round(rental_price + adjustment_val, 2)
			return self._calculated_rental_price
	
	def save(self, *args, **kwargs):
		rental_product = RentalProduct.objects.get(id=self.product.id)
		# Need to limit changes to rental after it has started
		self._rental_end_inc_turnaround = self.rental_end_inc_turnaround

		if self.rental_clash:
			raise ValidationError(_('This rental conflicts with another.'))

		if not self._fulfilled_rental_rate:
			self._fulfilled_rental_rate = self.fulfilled_rental_rate
		
		if not self._unfulfilled_rental_price:
			self._unfulfilled_rental_price = self.unfulfilled_rental_price
		return super().save(*args, **kwargs)


# Return a dry (uncommited) list of fulfilments to obtain pricing
def rental_fulfilment_price_factory(qs, rental_start, rental_end, fulfilment_date_time=timezone.now()):
	for idx, rp in enumerate(qs):
		rf = RentalFulfilment(product=rp, rental_start=rental_start, rental_end=rental_end)
		qs[idx].fulfilment_price = rf.fulfilment_price
	return qs


class RentalPriceAdjustment(PriceAdjustment):
	products = models.ManyToManyField(RentalProduct)


# Cant be changed within a month of rental
class RentalDriver(models.Model):
	class Status(models.TextChoices):
		APPROVED = 'APP', _('Approved')
		AWAITING_REVIEW = 'ARV', _('Awaiting Review')
		ACTION_REQUIRED = 'ARQ', _('Action Required')
		DENIED = 'DND', _('Denied')
		INCOMPLETE = 'INC', _('Incomplete')

	rental_fulfilment = models.ForeignKey(RentalFulfilment, null=False, blank=False, on_delete=models.CASCADE)
	status = models.CharField(max_length=3, choices=Status.choices, default=Status.AWAITING_REVIEW)
	first_name = models.CharField(max_length=150, null=False, blank=False)
	last_name = models.CharField(max_length=150, null=False, blank=False)
	dob = models.DateField(null=False, blank=False)
	licence_check_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='DVLA Check code', help_text=mark_safe('Click <a href="https://www.gov.uk/view-driving-licence" target="_blank"><u>HERE</u></a> for more information'))
	licence_front = CropItImageField(blank=True)
	licence_back = CropItImageField(blank=True)
	proof_of_address_1 = ScaleItImageField(blank=True)
	proof_of_address_2 = ScaleItImageField(blank=True)
	note = models.TextField(blank=True, null=True)

	@property
	def approved(self):
		if self.status == self.Status.APPROVED:
			return True
		return False

	@property
	def age(self):
		today = timezone.now()
		return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

	@property
	def status_class(self):
		return {
			self.Status.APPROVED: 'success',
			self.Status.AWAITING_REVIEW: 'info',
			self.Status.ACTION_REQUIRED: 'warning',
			self.Status.DENIED: 'danger',
			self.Status.INCOMPLETE: 'secondary',
		}.get(self.status, 'info')
	
	def clean_fields(self, *args, **kwargs):
		if self.age < 21:
			raise ValidationError({'dob': [_("Drivers must be over 21 years of age.")]})
		return super().clean_fields(*args, **kwargs)

	# Raise error if tying to change driver information after rental
	def clean(self, *args, **kwargs):
		if hasattr(self, 'rental_fulfilment'):
			if timezone.now() > self.rental_fulfilment.rental_start:
				raise ValidationError(_("Drivers cannot be edited after rental has commenced!"))
		return super().clean(*args, **kwargs)

	def save(self, *args, **kwargs):
		# Change status to incomplete if any fields are missing
		if (self.first_name is None
			or self.last_name is None
			or self.dob is None
			or self.licence_check_code is None
			or not self.licence_front.name
			or not self.licence_back.name
			or not self.proof_of_address_1.name
			or not self.proof_of_address_2.name):
				self.status = self.Status.INCOMPLETE
		else:
			if self.status not in {self.Status.APPROVED, self.Status.DENIED}:
				self.status = self.Status.AWAITING_REVIEW
		super().save(*args, **kwargs)

class RentalRules(models.Model):
	title = models.CharField(max_length=300, null=False, blank=False)
	description = models.TextField(null=True, blank=True)


class RentalInformation(models.Model):
	title = models.CharField(max_length=300, null=False, blank=False)
	description = models.TextField(null=True, blank=True)