import datetime

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from .models import (
	RentalFulfilment,
	RentalProduct
)
from .settings import RENTAL_CHECK_IN_TIME, RENTAL_CHECK_OUT_TIME

# Create your tests here.


# Test inserting overlapping rental inc min_turnaround
@override_settings(CHARGE_RENTAL_DAILY=True)
class RentalTestCase(TestCase):
	def setUpTestData(cls):
		cls.user1 = User.objects.create_user(username="test-user-1")
		cls.rp1 = RentalProduct.objects.create(
			slug='test-product-1',
			name='Test Product 1',
			description_short='Short Description of test product 1',
			description_long='Long Description of test product 1',
			base_price=100,
			qty=1,
			available=True,
			min_turnaround=3,
		)

		cls.rf1 = RentalFulfilment.objects.create(
			product=cls.rp1,
			fulfilling_user=cls.user1,
			rental_start=datetime.datetime.strptime('2022-03-03', '%Y-%m-%d'),
			rental_end=datetime.datetime.strptime('2022-03-06', '%Y-%m-%d'),
		)

	def test_rental_price(self):
		self.assertEqual(300, self.rf1.fulfilment_price) 

	def test_rental_price_inc_extras(self):
		pass

	def test_rental_price_inc_drivers(self):
		pass

	def test_rental_overlap(self):
		pass

	def test_rental_overlap_inc_turnaround(self):
		pass

	#Test whether conflict occurs when a rental is completely within the dates of another
	def test_rental_overlap_within(self):
		pass

	#Test whether conflict occurs when a rental is completely outside the dates of another
	def test_rental_overlap_outside(self):
		pass

	# test that check in time is applied when adding using form
	def test_check_in_applied(self):
		pass

	# test that check out time is applied when adding using form
	def test_check_in_applied(self):
		pass


