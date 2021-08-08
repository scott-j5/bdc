import datetime
import unittest

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase, SimpleTestCase, override_settings
from django.urls import path

from .utils import get_date_overlap, datediff_hours

# Create your tests here.
def response_error_handler(request, exception=None):
    return HttpResponse('Error handler content', status=403)


def permission_denied_view(request):
    raise PermissionDenied


urlpatterns = [
    path('403/', permission_denied_view),
]

handler403 = response_error_handler


# ROOT_URLCONF must specify the module that contains handler403 = ...
@override_settings(ROOT_URLCONF=__name__)
class CustomErrorHandlerTests(SimpleTestCase):

    def test_handler_renders_template_response(self):
        response = self.client.get('/403/')
        # Make assertions on the response here. For example:
        self.assertContains(response, 'Error handler content', status_code=403)


class TestUtils(unittest.TestCase):
	def test_get_date_overlap_start(self):
		range1 = [datetime.datetime(2021, 2, 10), datetime.datetime(2021, 2, 20)]
		range2 = [datetime.datetime(2021, 2, 1), datetime.datetime(2021, 2, 11)]
		overlap = get_date_overlap(range1, range2)
		self.assertEqual(overlap.days, 1)

	def test_get_date_overlap_end(self):
		range1 = [datetime.datetime(2021, 2, 10), datetime.datetime(2021, 2, 20)]
		range2 = [datetime.datetime(2021, 2, 15), datetime.datetime(2021, 2, 25)]
		overlap = get_date_overlap(range1, range2)
		self.assertEqual(overlap.days, 5)
	
	def test_get_date_overlap_internal(self):
		range1 = [datetime.datetime(2021, 2, 10), datetime.datetime(2021, 2, 20)]
		range2 = [datetime.datetime(2021, 2, 15), datetime.datetime(2021, 2, 16)]
		overlap = get_date_overlap(range1, range2)
		self.assertEqual(overlap.days, 1)

	def test_get_date_overlap_none(self):
		range1 = [datetime.datetime(2021, 2, 15), datetime.datetime(2021, 2, 20)]
		range2 = [datetime.datetime(2021, 2, 10), datetime.datetime(2021, 2, 15)]
		overlap = get_date_overlap(range1, range2)
		self.assertEqual(overlap, datetime.timedelta(0))

	def test_get_date_overlap_time(self):
		range1 = [datetime.datetime(2021, 2, 15, 0, 0, 0, 0), datetime.datetime(2021, 2, 20, 0, 0, 0, 0)]
		range2 = [datetime.datetime(2021, 2, 10, 0, 0, 0, 0), datetime.datetime(2021, 2, 15, 12, 0, 0, 0)]
		overlap = datediff_hours(get_date_overlap(range1, range2))
		self.assertEqual(overlap, 12)