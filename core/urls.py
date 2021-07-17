from django.urls import path, include, register_converter

from .views import (
	contact_view,
	faqs_view,
	home_view,
	pricing_view,
	testimonials_view,
)

#Custom regex url pattern match for an individual date eg. '/bookings/2021-12-12'
class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

#Custom regex url pattern match for a date range eg. '/bookings/2021-12-12-2021-12-15'
class DateRangeConverter:
    regex = '\d{4}-\d{2}-\d{2}-\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'date')
register_converter(DateRangeConverter, 'daterange')


urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
	path('contact/', contact_view, name='contact-us'),
	path('faqs/', faqs_view, name='faqs'),
	path('pricing/', faqs_view, name='pricing'),
	path('testimonials/', testimonials_view, name='testimonials'),
]