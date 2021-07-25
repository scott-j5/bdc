from core.forms import DateRangeFormMulti
from core.widgets import DatePicker
from core.layout import SpinnerSubmit
from crispy_forms.layout import (
	Layout,
	Field,
	Div,
	Submit
)
from django import forms


class FuilfilmentDateRangeForm(DateRangeFormMulti):
	fulfilment_date_time = forms.DateTimeField(widget=DatePicker(attrs={"placeholder": "Purchase Date", "data-flatpickr_args": {"enableTime": True,"dateFormat": "Y-m-dTH:i:S"}}), label=False, required=False)

	def clean(self, **kwargs):
		cleaned_data = super().clean(**kwargs)
		print(cleaned_data['fulfilment_date_time'])
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