from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.

class FaqCategory(models.Model):
	slug = models.SlugField(max_length=100, null=False, blank=False, unique=True)
	icon = models.CharField(max_length=150, null=False, blank=False, help_text=mark_safe("Available icon classes are available <a href='https://fontawesome.com/search?m=free'><u>HERE</u></a>"))
	name = models.CharField(max_length=100, null=False, blank=False, unique=True)
	description = models.TextField(null=False, blank=False)

	def __str__(self):
		return self.name

	def clean(self, *args, **kwargs):
		if self.slug == '' or self.slug == None:
			self.slug = self.name.replace(' ', '-').lower()
		super().clean(*args, **kwargs)	


class Faq(models.Model):
	category = models.ForeignKey(FaqCategory, null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=200, null=False, blank=False)
	description = models.TextField(null=False, blank=False)

	def __str__(self):
		return f'{self.category.name} - {self.title}'