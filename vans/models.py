from django.db import models
from imageit.models import ScaleItImageField

# Create your models here.
class Van(models.Model):
	slug = models.SlugField(blank=True, null=False)
	name = models.CharField(max_length=50, blank=False, null=False)
	description = models.TextField(null=True, blank=True)
	rate = models.IntegerField(default=0)
	registration = models.CharField(max_length=10)
	odo = models.IntegerField(default=0)
	available = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def clean(self):
		if not self.slug or self.slug == '':
			self.slug = self.name.replace(' ', '-').lower()

	#returns an array of unavailable days from today in format 'yyyy-mm-dd'
	def unavailable(self):
		return ['2021-07-25', '2021-07-26']


class VanPhotos(models.Model):
	def get_upload_path(instance, filename):
		return f'van_images/{self.van.slug}/{filename}'

	van = models.ForeignKey(Van, on_delete=models.CASCADE)
	photo = ScaleItImageField(max_width=1000, max_height=1000, quality=90, null=False, blank=False, upload_to=get_upload_path)
	banner = models.BooleanField(default=False)