from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML, Field, Submit

import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Product, ProductFeature, ProductImage


class ProductForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProductForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.form_id = 'product-update-form'
		self.helper.html5_required = True
		self.helper.layout = Layout(
            # Container for repeatable form groups (individual sitting requests)
                Div(
                    Row(
                        Column(
                            'name',
                            css_class='col-12 col-md-6',
                        ),
                        Column(
                            'slug',
                            css_class='col-12 col-md-6',
                        ),
                    ),
                    Row(
                        Column(
                            'description_short',
                            css_class="col-12 col-md-6"
                        ),
                        Column(
                            'description_long',
                            css_class="col-12 col-md-6"
                        ),
                    ),
                    Row(
                        Column(
							'base_price',
							css_class="col-md-4"
						),
						Column(
							'available',
							css_class="col-md-4 d-flex justify-content-center"
						),
						css_class="align-items-center"
                    ),
                ),
            )

	class Meta:
		model = Product
		fields = ['name', 'slug', 'description_short', 'description_long', 'base_price', 'available', 'qty']


class ProductImageFormHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.form_method = 'POST'
		self.form_id = 'product-image-update-form'
		self.html5_required = True
		self.layout = Layout(
            # Container for repeatable form groups (individual sitting requests)
                Div(
                    Row(
                        Column(
                            'image',
                            css_class='col-12 col-md-8',
                        ),
						Column(
							Column(
								'product',
								css_class='col-12',
							),
							Column(
								'primary',
								css_class='col-12',
							),
							Column(
								'banner',
								css_class='col-12',
							),
							Column(
								'thumbnail',
								css_class='col-12 mb-0',
							),
							css_class='col-12 col-md-4',
						),
                    ),
					css_class="border-top mb-3 pt-3"
                ),
            )


class ProductImageForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProductImageForm, self).__init__(*args, **kwargs)
		self.helper = ProductImageFormHelper()

	class Meta:
		model = ProductImage
		fields = ['image', 'product', 'primary', 'banner', 'thumbnail']

ProductImageFormSet = forms.formset_factory(form=ProductImageForm, extra=1)



class ProductFeatureFormHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.form_method = 'POST'
		self.form_id = 'product-feature-update-form'
		self.html5_required = True
		self.layout = Layout(
            # Container for repeatable form groups (individual sitting requests)
                Div(
                    Row(
                        Column(
                            'name',
                            css_class='col-12 col-md-6',
                        ),
                        Column(
                            'icon_class',
                            css_class='col-12 col-md-6',
                        ),
                    ),
                    Row(
                        Column(
                            'description',
                            css_class="col-12 mb-0"
                        ),
                    ),
					css_class="border-top mb-3 pt-3"
                ),
            )


class ProductFeatureForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProductFeatureForm, self).__init__(*args, **kwargs)
		self.fields['description'].widget.attrs = {'rows':1}
		self.helper = ProductFeatureFormHelper()

	class Meta:
		model = ProductFeature
		fields = ['name', 'description', 'icon_class']

ProductFeatureFormSet = forms.formset_factory(form=ProductFeatureForm, extra=1)