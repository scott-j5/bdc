from django.db import models
from imageit.models import ScaleItImageField

# Create your models here.
class Van(models.Model):
	slug = models.SlugField(blank=False, null=False)
	name = models.CharField(max_length=50, blank=False, null=False)
	Description = models.TextField(null=True, blank=True)
	rate = models.IntegerField(default=0)
	registration = models.CharField(max_length=10)
	odo = models.IntegerField(default=0)
	available = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if not self.slug or self.slug == '':
			self.slug = self.name.replace(' ', '-')
		return super.save(self, *args, **kwargs)


class VanPhotos(models.Model):
	def get_upload_path(instance, filename):
		return f'van_images/{self.van.slug}/{filename}'

	van = models.ForeignKey(Van, on_delete=models.CASCADE)
	photo = ScaleItImageField(max_width=1000, max_height=1000, quality=90, null=False, blank=False, upload_to=get_upload_path)
	banner = models.BooleanField(default=False)