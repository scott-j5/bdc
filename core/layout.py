from crispy_forms.layout import Submit

class SpinnerSubmit(Submit):
	template = "core/custom_crispy_templates/layout/spinner_submit_button.html"

	def __init__(self, *args, **kwargs):
		self.icon = kwargs.pop('icon') if kwargs.get('icon') is not None else ''
		super().__init__(*args, **kwargs)