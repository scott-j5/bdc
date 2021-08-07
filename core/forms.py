from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import PrependedText
from crispy_forms.layout import (
	Layout,
	Field,
	Div,
	Submit
)
from django import forms
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from.layout import SpinnerSubmit
from .utils import parse_date_range
from .widgets import DatePicker, DateRangePicker

class ContactForm(forms.Form):
	full_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	message = forms.CharField(widget=forms.Textarea)
	recaptcha = ReCaptchaField()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.form_action = reverse_lazy('contact-us')
		self.helper.form_id = 'contact-us-form'
		self.helper.html5_required = True
		self.helper.layout = Layout (
			Div(
				Div(
					Div(
						'full_name',
						css_class="col-12 col-md-6"
					),
					Div(
						'email',
						css_class="col-12 col-md-6"
					),
					css_class="row"
				),
				Div(
					Div(
						'message',
						css_class="col-12"
					),
					css_class="row"
				),
				Div(
					Div(
						'recaptcha',
						css_class="col-12 col-md-6"
					),
					Div(
						SpinnerSubmit("send", "Send Message", css_class='crispy-btn mb-0'),
						css_class="col-12 col-md-6 d-flex justify-content-center"
					),
					css_class="row align-items-center"
				),
				css_class=""
			)
		)


class DateRangeForm(forms.Form):
	check_in = forms.DateTimeField(widget=DatePicker(attrs={"placeholder": "Check In"}), label=False, required=False)
	check_out = forms.DateTimeField(widget=DatePicker(attrs={"placeholder": "Check Out"}), label=False, required=False)

	def __init__(self, *args, **kwargs):
		#Set Default attrs for the flatpickr input
		widget_attrs = {
			"placeholder": "Check In - Check Out",
			"class": "datepicker",
		}
		flatpickr_args = {}
		
		# Allow custom form action to be set on init defaults to #
		action = kwargs.pop('action') if kwargs.get('action') is not None else '#'

		#Allow custom submit button value
		self.submit_value = kwargs.pop('submit_text') if kwargs.get('submit_text') is not None else "Search"

		#Set Widget args from kwargs
		if kwargs.get('widget_attrs') is not None:
			if not type(kwargs.get('widget_attrs')) is dict:
				raise ImproperlyConfigured(_("Widget atrributes must be passed as a dict object"))
			else:
				widget_attrs.update(kwargs.pop('widget_attrs'))

		#Set Flatpickr args from kwargs
		if kwargs.get('flatpickr_args') is not None:
			if not type(kwargs.get('flatpickr_args')) is dict:
				raise ImproperlyConfigured(_("Flatpicker arguments must be passed as a dict object"))
			else:
				flatpickr_args.update(kwargs.pop('flatpickr_args'))

		super().__init__(*args, **kwargs)

		widget_attrs.update({"data-flatpickr_args": flatpickr_args})
		self.fields['stay'] = forms.CharField(widget=DateRangePicker(attrs=widget_attrs), required=True)
		self.fields['stay'].label = False
		self.helper = FormHelper()
		self.helper.form_method = 'GET'
		self.helper.form_action = action
		self.helper.form_id = 'date-search-form'
		self.helper.html5_required = True
		self._layout()

	def _layout(self):
		self.helper.layout = Layout (
			Div(
				Div(
					Div(
						'stay',
						css_class="col-12 col-md-6",
					),
					Div(
						SpinnerSubmit("search", self.submit_value, css_class='crispy-btn btn-danger', icon='<i class="icon-125" data-feather="search"></i>'),
						css_class="d-grid col-12 col-md-6"
					),
					css_class="row"
				),
			)
		)
	
	def clean(self):
		cleaned_data = super().clean()
		stay = cleaned_data.get('stay')

		if len(stay.split(" to ")) != 2:
			raise ValidationError(_("Please provide a check out date."))
		else:
			range_list = parse_date_range(stay)
			cleaned_data['check_in'] = range_list[0]
			cleaned_data['check_out'] = range_list[1]
		return cleaned_data


class DateRangeFormMulti(DateRangeForm):
	def __init__(self, *args, **kwargs):
		#Set Default attrs for the flatpickr input
		widget_attrs = {
			"placeholder": "Check In",
			"data-range_second_input": "#check_out_date"
		}

		#Set Flatpickr args from kwargs
		if kwargs.get('widget_attrs') is not None and type(flatpickr_args) is dict:
			widget_attrs.update(kwargs.pop('widget_attrs'))
		super().__init__(*args, **kwargs, widget_attrs=widget_attrs)

	def _layout(self):
		self.helper.layout = Layout (
			Div(
				Div(
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
						css_class="d-grid col-12 col-md-4"
					),
					css_class="row"
				),
			)
		)