import json

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TextInput, MultiWidget


class DatePicker(TextInput):
	
	def __init__(self, attrs=None):
		new_attrs = {} if attrs is None else attrs
		class_defaults = 'datepicker'
		flatpickr_defaults = {
				"minDate": "today",
				"position": "auto center",
				"altInput": True,
				"altFormat": "F j, Y",
				"dateFormat": "Y-m-d",
			}
		#For time input "enableTime": True,"dateFormat": "Y-m-dTH:i:S",

		#If additional flatpickr configs are passed apply them
		if new_attrs.get('data-flatpickr_args') is not None:
			if type(new_attrs.get('data-flatpickr_args')) is dict:
				flatpickr_defaults.update(new_attrs.get('data-flatpickr_args'))
			else:
				raise ImproperlyConfigured(_("Flatpickr Widget arguments must be passed as a dict object"))
		
		#Dump flatpickr attributes
		new_attrs['data-flatpickr_args'] = json.dumps(flatpickr_defaults)
		
		new_attrs['class'] = class_defaults if new_attrs.get('class') is None else new_attrs.get('class') + ' ' + class_defaults
		super().__init__(new_attrs)


class DateRangePicker(DatePicker):

	def __init__(self, attrs=None):
		# Ensure flatpickr is initialised in range mode
		if type(attrs) is dict:
			if attrs.get('data-flatpickr_args') is not None:
				attrs['data-flatpickr_args'].update({'mode': 'range'})
			else:
				attrs['data-flatpickr_args'] = {'mode': 'range'}
		else:
			if attrs is not None:
				raise ImproperlyConfigured(_("Date Range Widget arguments must be passed as a dict object"))
		super().__init__(attrs)