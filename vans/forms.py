from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
	Layout,
	Div,
)
from django.forms import(
	Form,
	ModelForm,
)

from .models import Van


class VanForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout (
			'name',
			'rate',
			'registration',
			'odo',
		)

	class Meta:
		model = Van
		fields = ['name', 'rate', 'registration', 'odo']