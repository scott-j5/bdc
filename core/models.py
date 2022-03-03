from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class FaqCategory(models.Model):
	slug = models.SlugField(max_length=100, null=False, blank=False, unique=True)
	icon = models.CharField(max_length=150, null=False, blank=False)
	name = models.CharField(max_length=100, null=False, blank=False, unique=True)
	description = models.TextField(null=False, blank=False)

	def __str__(self):
		return self.name

class Faq(models.Model):
	category = models.ForeignKey(FaqCategory, null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=200, null=False, blank=False)
	description = models.TextField(null=False, blank=False)

	def __str__(self):
		return f'{self.category.name} - {self.title}'