
from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML, Field, Submit
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from core.forms import DateRangeFormMulti, DateRangeForm
from core.widgets import DatePicker
from core.layout import SpinnerSubmit
from crispy_forms.layout import (
	Layout,
	Field,
	Div,
	Submit
)

from .settings import RENTAL_CHECK_IN_TIME, RENTAL_CHECK_OUT_TIME
from .models import RentalFulfilment, RentalProduct


class RentalDateRangeForm(DateRangeForm):
	def clean(self, *args, **kwargs):
		cleaned_data = super().clean(*args, **kwargs)
		cleaned_data['check_in'] = datetime.combine(cleaned_data['check_in'].date(), RENTAL_CHECK_IN_TIME)
		cleaned_data['check_out'] = datetime.combine(cleaned_data['check_out'].date(), RENTAL_CHECK_OUT_TIME)
		if (cleaned_data['check_out'] - cleaned_data['check_in']).total_seconds() <= 0:
			raise ValidationError(_("Check out must not be before Check in."))
		return cleaned_data


class FuilfilmentDateRangeForm(DateRangeFormMulti):
	fulfilment_date_time = forms.DateTimeField(widget=DatePicker(attrs={"placeholder": "Purchase Date", "data-flatpickr_args": {"enableTime": True,"dateFormat": "Y-m-dTH:i:S"}}), label=False, required=False)

	def clean(self, **kwargs):
		cleaned_data = super().clean(**kwargs)
		return cleaned_data

	def _layout(self):
		self.helper.layout = Layout (
			Div(
				Div(
					Div(
						'fulfilment_date_time',
						css_class="col-12 col-md-4",
					),
					Div(
						'stay',
						css_class="col-12 col-md-4",
					),
					Div(
						Field('check_out', id="check_out_date"),
						css_class="col-12 col-md-4",
					),
					Div(
						SpinnerSubmit("search", self.submit_value, css_class='crispy-btn btn-danger', icon='<i class="icon-125" data-feather="search"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				),
			)
		)


class RentalFulfilmentCreateForm(forms.ModelForm):
	#If staff show field to add rental for someone else set to request.user
	product = forms.ModelChoiceField(queryset=RentalProduct.objects.all())
	rental_start = forms.DateTimeField(widget=DatePicker(attrs={"placeholder": "Rental Start", "data-flatpickr_args": {"enableTime": True,"dateFormat": "Y-m-dTH:i:S"}}), label=False, required=False)
	rental_end = forms.DateTimeField(widget=DatePicker(attrs={"placeholder": "Rental End", "data-flatpickr_args": {"enableTime": True,"dateFormat": "Y-m-dTH:i:S"}}), label=False, required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_action = reverse_lazy('rental-fulfilment-add')
		self.helper.form_method = 'POST'
		self.helper.form_id = 'rental-fulfilment-create-form'
		self.helper.html5_required = False
		self.helper.layout = Layout(
            Div(
				Div(
					Div(
						'product',
						css_class="col-12",
					),
					Div(
						'rental_start',
						css_class="col-12",
					),
					Div(
						'rental_end',
						css_class="col-12",
					),
					Div(
						SpinnerSubmit("submit", 'Continue', css_class='crispy-btn btn-danger', icon='<i class="icon-125" data-feather="chevrons-right"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				),
			)
		)

	class Meta:
		model = RentalFulfilment
		fields = ['product', 'rental_start', 'rental_end']


class AdminRentalFulfilmentCreateForm(RentalFulfilmentCreateForm):
	#If staff show field to add rental for someone else set to request.user

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super().__init__(*args, **kwargs)
		self.helper.html5_required = True
		self.helper.layout = Layout(
            Div(
				Div(
					Div(
						'fulfilling_user',
						css_class="col-12",
					),
					Div(
						'product',
						css_class="col-12",
					),
					Div(
						'rental_start',
						css_class="col-12",
					),
					Div(
						'rental_end',
						css_class="col-12",
					),
					Div(
						SpinnerSubmit("submit", 'Continue', css_class='crispy-btn btn-danger', icon='<i class="icon-125" data-feather="chevrons-right"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				),
			)
		)

	def clean(self, *args, **kwargs):
		# If user is not staff and tried to set fulfilling_user raise error
		# If user not staff set fulfilling_user to requesting user
		if not self.request.user.is_staff:
			if self.fields['fulfilling_user'].value is not None:
				raise ValidationError(_('Disallowed operation'), code='invalid')
			else:
				self.fields['fulfilling_user'].value = self.request.user
		return super().clean(*args, **kwargs)

	class Meta:
		model = RentalFulfilment
		fields = ['fulfilling_user', 'product', 'rental_start', 'rental_end']


class RentalFulfilmentExtrasForm(forms.ModelForm):
	class Meta:
		model = RentalFulfilment
		fields = ['rental_extras']