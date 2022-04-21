
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML, Field, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from imageit.fields import CropItImageFormField

from core.widgets import DatePicker

from .models import UserProfile

class SignupForm(forms.Form):
	flatpickr_args = {"data-flatpickr_args": {"minDate": '1800-01-01', "maxDate": 'today'}}
	avatar = CropItImageFormField()
	first_name = forms.CharField()
	last_name = forms.CharField
	dob = forms.DateField(widget=DatePicker(attrs=flatpickr_args))

	def __init__(self, *args, **kwargs):
		pass

	def signup(self, request, user):
		pass


class UserUpdateForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'user-form'
		self.helper.html5_required = True
		self.helper.form_tag = False
		self.helper.layout = Layout (
			Div(
				Div(
					Div(
						'first_name',
						css_class="col-12 col-md-6"
					),
					Div(
						'last_name',
						css_class="col-12 col-md-6"
					),
					css_class="row"
				),
				css_class=""
			)
		)

	class Meta:
		model = User
		fields = ['first_name', 'last_name']


class UserProfileUpdateForm(forms.ModelForm):
	flatpickr_args = {"data-flatpickr_args": {"minDate": '1800-01-01', "maxDate": 'today'}}
	dob = forms.DateField(widget=DatePicker(attrs=flatpickr_args))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'user-form'
		self.helper.form_tag= False
		self.helper.html5_required = True
		self.helper.layout = Layout (
			Div(
				Div(
					Div(
						'dob',
						css_class="col-12 col-md-6"
					),
					css_class="row"
				),
				Div(
					Div(
						'avatar',
						css_class="col-12"
					),
					css_class="row",
				),
				css_class=""
			)
		)

	def clean(self, *args, **kwargs):
		cleaned_data = super().clean(*args, **kwargs)
		if cleaned_data['dob'] > timezone.now().date():
			raise ValidationError(_("Not a valid Date of Birth"))
		return cleaned_data

	class Meta:
		model = UserProfile
		fields = ['avatar', 'dob']