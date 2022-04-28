
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML, Field, Submit
from django import forms
from django.urls import reverse_lazy

from core.layout import SpinnerSubmit

from .models import Faq, FaqCategory

class FaqForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'faq-create-form'
		self.helper.html5_required = False
		if self.instance.pk is not None:
			self.helper.form_action = reverse_lazy('faq-update', kwargs={'pk': self.instance.id})
			self.helper.layout = Layout(
				Div(
					Div(
						'category',
						css_class='col-12 col-md-6'
					),
					Div(
						'title',
						css_class='col-12 col-md-6'
					),
					Div(
						'description',
						css_class='col-12'
					),
					Div(
						SpinnerSubmit("submit", 'Update', css_class='crispy-btn btn-danger', icon='<i class="fa fa-check"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				)
			)
		else:
			self.helper.form_action = reverse_lazy('faq-add')
			self.helper.layout = Layout(
				Div(
					Div(
						'category',
						css_class='col-12 col-md-6'
					),
					Div(
						'title',
						css_class='col-12 col-md-6'
					),
					Div(
						'description',
						css_class='col-12'
					),
					Div(
						SpinnerSubmit("submit", 'Add', css_class='crispy-btn btn-danger', icon='<i class="fa fa-check"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				)
			)

	class Meta:
		model = Faq
		fields = ['category', 'title', 'description']


class FaqCategoryForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		
		self.helper.form_id = 'faq-category-create-form'
		self.helper.html5_required = False

		if self.instance.pk is not None:
			self.helper.form_action = reverse_lazy('faq-category-update', kwargs={'pk': self.instance.pk})
			self.helper.layout = Layout(
				Div(
					Div(
						'name',
						css_class='col-12 col-md-6'
					),
					Div(
						'icon',
						css_class='col-12 col-md-6'
					),
					Div(
						'description',
						css_class='col-12'
					),
					Div(
						SpinnerSubmit("submit", 'Update', css_class='crispy-btn btn-danger', icon='<i class="fa fa-check"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				)
			)
		else:
			self.helper.form_action = reverse_lazy('faq-category-add')
			self.helper.layout = Layout(
				Div(
					Div(
						'name',
						css_class='col-12 col-md-6'
					),
					Div(
						'icon',
						css_class='col-12 col-md-6'
					),
					Div(
						'description',
						css_class='col-12'
					),
					Div(
						SpinnerSubmit("submit", 'Add', css_class='crispy-btn btn-danger', icon='<i class="fa fa-check"></i>'),
						css_class="d-grid col-12"
					),
					css_class="row"
				)
			)

	class Meta:
		model = FaqCategory
		fields = ['icon', 'name', 'description']