from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import PrependedText
from crispy_forms.layout import (
	Layout,
	Div,
	Submit
)
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from.layout import SpinnerSubmit
from .widgets import DateRangePicker

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
						Submit("send", "Send Message", css_class='crispy-btn mb-0'),
						css_class="col-12 col-md-6 d-flex justify-content-center"
					),
					css_class="row align-items-center"
				),
				css_class=""
			)
		)


class DateRangeForm(forms.Form):
	start_date = forms.DateField()
	end_date = forms.DateField()

	def __init__(self, *args, **kwargs):
		# Allow custom form action to be set on init defaults to #
		if kwargs.get('action') is not None:
			action = kwargs.pop('action')
		else:
			action = '#'

		#Set Default attrs for the date input
		attrs = {'placeholder': 'Date', "class": "datepicker"}

		#Set args for flatpickr date selector
		if kwargs.get('flatpickr_args') is not None:
			if type(kwargs.get('flatpickr_args')) is dict:
				attrs.update({'data-flatpickr_args': kwargs.pop('flatpickr_args')})
			else:
				raise ImproperlyConfigured(_("Flatpicker arguments must be passed as a dict object"))
			

		super().__init__(*args, **kwargs)

		self.fields['date_range'] = forms.CharField(widget=DateRangePicker(attrs=attrs))
		self.fields['date_range'].label = False
		self.helper = FormHelper()
		self.helper.form_method = 'GET'
		self.helper.form_action = reverse_lazy(action)
		self.helper.form_id = 'date-search-form'
		self.helper.html5_required = True
		self.helper.layout = Layout (
			Div(
				Div(
					Div(
						'date_range',
						css_class="col-12 col-md-6"
					),
					Div(
						SpinnerSubmit("search", "Search", css_class='crispy-btn mb-0 spinner-btn'),
						css_class="col-12 col-md-6"
					),
					css_class="row"
				),
				css_class=""
			)
		)
	
	def clean(self):
		cleaned_data = super().clean()

		return cleaned_data