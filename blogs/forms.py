import os
from collections import namedtuple
from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML, Field, Submit

from .models import Blog, BlogImage

class BlogImageForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		if kwargs.get('blog_slug'):
			self.blog_slug = kwargs.pop('blog_slug')
		super(BlogImageForm, self).__init__(**kwargs)

	def save(self, commit=True):
		instance = super().save(commit=False)

		if commit:
			try:
				instance.blog = Blog.objects.get(slug=self.blog_slug)
			except Blog.DoesNotExist:
				instance.blog = None

			instance = super().save()
			return reverse_lazy('blog-image', args=[instance.id])

		# If `commit is False`, return the path and in-memory image.
		image_data = namedtuple('image_data', ['path', 'image'])
		return image_data(path=instance.image.url, image=instance.image)

	class Meta:
		model = BlogImage
		fields = ['image',]


# Start Sitting Request forms
class BlogForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BlogForm, self).__init__(*args, **kwargs)
		self.fields['tags'].required = False
		self.helper = FormHelper()
		self.helper.form_action = reverse_lazy('blog-update', kwargs={'slug': self.instance.slug})
		self.helper.form_method = 'POST'
		self.helper.form_id = 'blog-form'
		self.helper.layout = Layout(
			Div(
				Row(
					Column(
						'title',
						css_class='col-12 col-md-6'
					),
					Column(
						'slug',
						css_class='col-12 col-md-6'
					),
				),
				Row(
					Column(
						'author',
						css_class='col-12 col-md-6'
					),
					Column(
						Div(
							'published', 
							css_class="align-self-end"
						),
						css_class='col-12 col-md-6 d-flex'
					),
				),
				Row(
					Column(
						'description',
						css_class='col-12'
					),
				),
				Row(
					Column(
						'tags',
						css_class='col-12'
					),
				),
				Row(
					Column(
						'thumbnail',
						css_class='col-12'
					),
				),
				Row(
					Column(
						'banner',
						css_class='col-12'
					),
				),
				Row(
					Column(
						'content',
						css_class='col-12'
					),
				),
			),
		)
		self.helper.add_input(Submit("submit", "Save changes", css_class='crispy-btn'))
		
	class Meta:
		model = Blog
		fields = ['author', 'published', 'title', 'slug', 'description', 'thumbnail', 'banner', 'tags', 'content']
