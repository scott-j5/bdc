import json
from django.forms.widgets import TextInput, MultiWidget


class DatePicker(TextInput):
	
	def __init__(self, attrs=None):
		defaults = {
				"minDate": "today",
				"position": "auto center",
				"altInput": True,
				"altFormat": "F j, Y",
				"dateFormat": "Y-m-d",
			}
		#For time input "enableTime": True,"dateFormat": "Y-m-dTH:i:S",


		#If additional flatpickr configs are passed apply them
		if attrs.get('data-flatpickr_args') is not None:
			defaults.update(attrs.get('data-flatpickr_args'))

		attrs['data-flatpickr_args'] = json.dumps(defaults)
		return super().__init__(attrs)


class DateRangePicker(DatePicker):

	def __init__(self, attrs=None):
		# Ensure flatpickr is initialised in range mode
		if attrs.get('data-flatpickr_args') is not None:
			attrs['data-flatpickr_args'].update({'mode': 'range'})
		return super().__init__(attrs)