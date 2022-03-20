from crispy_forms.layout import Submit
from crispy_forms.utils import TEMPLATE_PACK

class SpinnerSubmit(Submit):
	template = "core/custom_crispy_templates/layout/spinner_submit_button.html"

	def __init__(self, *args, **kwargs):
		self.icon = kwargs.pop('icon') if kwargs.get('icon') is not None else ''
		super().__init__(*args, **kwargs)
		self.template = "core/custom_crispy_templates/layout/spinner_submit_button.html"


class SpinnerSubmitBlock(Submit):
	template = "core/custom_crispy_templates/layout/spinner_submit_button_block.html"

	def __init__(self, *args, **kwargs):
		self.icon = kwargs.pop('icon') if kwargs.get('icon') is not None else ''
		super().__init__(*args, **kwargs)