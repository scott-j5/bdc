
from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML, Field, Submit
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _

from core.forms import DateRangeFormMulti, DateRangeForm
from core.layout import SpinnerSubmit, SpinnerSubmitBlock
from core.utils import parse_date_range
from core.widgets import DatePicker, DateRangePicker

from .settings import RENTAL_CHECK_IN_TIME, RENTAL_CHECK_OUT_TIME
from .models import RentalDriver, RentalExtra, RentalFulfilment, RentalProduct


class RentalDateRangeForm(DateRangeForm):
	def clean(self, *args, **kwargs):
		cleaned_data = super().clean(*args, **kwargs)
		if RENTAL_CHECK_IN_TIME:
			cleaned_data['check_in'] = make_aware(datetime.combine(cleaned_data['check_in'].date(), RENTAL_CHECK_IN_TIME))
		if RENTAL_CHECK_OUT_TIME:
			cleaned_data['check_out'] = make_aware(datetime.combine(cleaned_data['check_out'].date(), RENTAL_CHECK_OUT_TIME))
		if (cleaned_data['check_out'] - cleaned_data['check_in']).total_seconds() <= 0:
			raise ValidationError(_("Check out must not be before Check in."))
		return cleaned_data


class RentalDateRangeFormMulti(DateRangeFormMulti):
	def clean(self, *args, **kwargs):
		cleaned_data = super().clean(*args, **kwargs)
		if RENTAL_CHECK_IN_TIME:
			cleaned_data['check_in'] = make_aware(datetime.combine(cleaned_data['check_in'].date(), RENTAL_CHECK_IN_TIME))
		if RENTAL_CHECK_OUT_TIME:
			cleaned_data['check_out'] = make_aware(datetime.combine(cleaned_data['check_out'].date(), RENTAL_CHECK_OUT_TIME))
		if (cleaned_data['check_out'] - cleaned_data['check_in']).total_seconds() <= 0:
			raise ValidationError(_("Check out must not be before Check in."))
		return cleaned_data


class RentalProductDateRangeForm(RentalDateRangeForm):
	product = forms.ModelChoiceField(queryset=RentalProduct.objects.all())

	def clean(self, *args, **kwargs):
		cleaned_data = super().clean(*args, **kwargs)
		if not cleaned_data["product"].is_available(cleaned_data["check_in"], cleaned_data["check_out"]):
			raise ValidationError(_("This Product is not available for the selected dates"))


class RentalFuilfilmentDateRangeForm(RentalDateRangeFormMulti):
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
		self.request = kwargs.pop('request', None)
		hidden = kwargs.pop('hidden', False)
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_action = reverse_lazy('rental-fulfilment-add')
		self.helper.form_id = 'rental-fulfilment-create-form'
		self.helper.html5_required = False
		if hidden:
			self.helper.layout = Layout(
				Div(
					Div(
						Div(
							Field(
								'product',
								type="hidden",
							),
							Field(
								'rental_start',
								type="hidden",
							),
							Field(
								'rental_end',
								type="hidden",
							),
						),
						Div(
							SpinnerSubmit("submit", 'Book Now', css_class='crispy-btn btn-danger', icon='<i class="icon-125" data-feather="chevrons-right"></i>'),
							css_class="d-grid col-12"
						),
						css_class="row"
					),
				)
			)
		else:
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
		request = kwargs.pop('request', None)
		super().__init__(*args, **kwargs)
		self.request = request
		print(self.request.user)
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


class RentalFulfilmentExtraInformationForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_action = reverse_lazy('rental-fulfilment-extra-information', kwargs={'pk':self.instance.id})
		self.helper.form_method = 'POST'
		self.helper.form_id = 'rental-fulfilment-extra-information-form'
		self.helper.html5_required = True
		self.helper.layout = Layout(
            Div(
				Div(
					Div(
						'pickup_location',
						css_class="col-12",
					),
					Div(
						'pickup_address',
						css_class="col-12",
					),
					Div(
						SpinnerSubmit("submit", 'Save & Continue', css_class='crispy-btn btn-danger', icon='<i class="icon-125" data-feather="chevrons-right"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				),
			)
		)

	class Meta: 
		model = RentalFulfilment
		fields = ['pickup_location', 'pickup_address']


class RentalFulfilmentExtrasForm(forms.ModelForm):
	rental_extras = forms.ModelMultipleChoiceField(queryset=RentalExtra.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_action = reverse_lazy('rental-fulfilment-extras', kwargs={'pk':self.instance.id})
		self.helper.form_method = 'POST'
		self.helper.form_id = 'rental-fulfilment-extras-form'
		self.helper.html5_required = True
		self.helper.layout = Layout(
            Div(
				Div(
					Div(
						'rental_extras',
						css_class="col-12",
					),
					Div(
						SpinnerSubmit("submit", 'Save & Continue', css_class='crispy-btn btn-danger', icon='<i class="icon-125" data-feather="chevrons-right"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				),
			)
		)

	class Meta: 
		model = RentalFulfilment
		fields = ['rental_extras']


class RentalFulfilmentFilterForm(forms.ModelForm):
	status_choices = [(None,'---------')] + RentalFulfilment.Status.choices
	product = forms.ModelChoiceField(queryset=RentalProduct.objects.all(), required=False)
	status = forms.ChoiceField(choices=status_choices, required=False)
	fulfilment_date_range = forms.CharField(label='Purchase Date' , widget=DateRangePicker(attrs={"placeholder": "Select Range", 'data-flatpickr_args': {'minDate': False}}), required=False)
	rental_start_range = forms.CharField(label='Check in Range', widget=DateRangePicker(attrs={"placeholder": "Select Range", 'data-flatpickr_args': {'minDate': False}}), required=False)
	rental_end_range = forms.CharField(label='Check out Range', widget=DateRangePicker(attrs={"placeholder": "Select Range", 'data-flatpickr_args': {'minDate': False}}), required=False)

	def __init__(self, *args, **kwargs):
		form_action_name = kwargs.pop('form_action_name', None)
		super().__init__(*args, **kwargs)
		self.fields['fulfilling_user'].required = False

		self.helper = FormHelper()
		if form_action_name is not None:
			self.helper.form_action = reverse_lazy(form_action_name)
		self.helper.form_method = 'GET'
		self.helper.form_id = 'rental-fulfilment-filter-form'
		self.helper.html5_required = True
		self.helper.layout = Layout(
            Div(
				Div(
					Div(
						'product',
						css_class="col-12 col-md-4",
					),
					Div(
						'fulfilling_user',
						css_class="col-12 col-md-4",
					),
					Div(
						'status',
						css_class="col-12 col-md-4",
					),
					css_class="row"
				),
				Div(
					Div(
						'fulfilment_date_range',
						css_class="col-12 col-md-4"
					),
					Div(
						'rental_start_range',
						css_class="col-12 col-md-4"
					),
					Div(
						'rental_end_range',
						css_class="col-12 col-md-4"
					),
					css_class="row"
				),
				Div(
					Div(
						HTML('<a class="btn btn-default" href="{%% url \'%s\' %%}">Clear Filters</a>' % (form_action_name)),
						css_class="d-grid col-12 col-md-6"
					),
					Div(
						SpinnerSubmit("submit", 'Update', css_class='crispy-btn btn-danger', icon='<i class="fa fa-search"></i>'),
						css_class="d-grid col-12 col-md-6"
					),
					css_class="row"
				),
			)
		)

	class Meta:
		model = RentalFulfilment
		fields = ['fulfilling_user', 'product', 'status']


class RentalDriverAddForm(forms.ModelForm):
	dob = forms.DateField(widget=DatePicker(attrs={"placeholder": "", "data-flatpickr_args": {"minDate": False, "maxDate": 'today'}}))

	def __init__(self, *args, **kwargs):
		self.rental_fulfilment_id = kwargs.pop('rental_fulfilment_id', None)
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_action = self.get_form_action()
		self.helper.form_method = 'POST'
		self.helper.form_id = 'rental-fulfilment-drivers-form'
		self.helper.html5_required = False
		self.helper.layout = Layout(
            Div(
				Div(
					Div(
						'first_name',
						css_class="col-12 col-md-6",
					),
					Div(
						'last_name',
						css_class="col-12 col-md-6",
					),
					Div(
						'dob',
						css_class="col-12 col-md-6",
					),
					Div(
						'licence_check_code',
						css_class="col-12 col-md-6",
					),
					Div(
						'licence_front',
						css_class="col-12 col-md-6",
					),
					Div(
						'licence_back',
						css_class="col-12 col-md-6",
					),
					Div(
						'proof_of_address_1',
						css_class="col-12 col-md-6",
					),
					Div(
						'proof_of_address_2',
						css_class="col-12 col-md-6",
					),
					Div(
						SpinnerSubmit("submit", 'Confirm Driver', css_class='crispy-btn btn-danger', icon='<i class="fa fa-check"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				),
			)
		)

	def get_form_action(self):
		return reverse_lazy('rental-fulfilment-driver-add', kwargs={'rental_pk':self.rental_fulfilment_id})

	class Meta:
		model = RentalDriver
		fields = ['first_name', 'last_name', 'dob', 'licence_check_code', 'licence_front', 'licence_back', 'proof_of_address_1', 'proof_of_address_2']


class RentalDriverUpdateForm(RentalDriverAddForm):		
	def get_form_action(self):
		return reverse_lazy('rental-fulfilment-driver-update', kwargs={'rental_pk': self.instance.rental_fulfilment.id, 'pk':self.instance.id})


class RentalDriverFormsetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		rental_fulfilment_id = kwargs.pop('rental_fulfilment_id', None)
		super().__init__(*args, **kwargs)
		self.form_action = reverse_lazy('rental-fulfilment-drivers', kwargs={'pk':rental_fulfilment_id})
		self.form_method = 'POST'
		self.form_id = 'rental-fulfilment-drivers-form'
		self.html5_required = False
		self.layout = Layout(
            Div(
				Div(
					Div(
						'first_name',
						css_class="col-12 col-md-4",
					),
					Div(
						'last_name',
						css_class="col-12 col-md-4",
					),
					Div(
						'dob',
						css_class="col-12 col-md-4",
					),
					Div(
						'licence_front',
						css_class="col-12 col-md-6",
					),
					Div(
						'licence_back',
						css_class="col-12 col-md-6",
					),
					HTML(
						"<hr/>",
					),
					css_class="row",
				),
				css_class='formset-group',
			)
		)
		self.add_input(SpinnerSubmit("submit", 'Continue', css_class='crispy-btn btn-danger float-end', icon='<i class="icon-125" data-feather="chevrons-right"></i>', template="core/custom_crispy_templates/spinner_submit_button.html"))
		

RentalDriverFormSet = forms.formset_factory(RentalDriverUpdateForm, extra=2, can_delete=True)
