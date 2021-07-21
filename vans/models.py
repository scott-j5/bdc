from django.db import models
from imageit.models import ScaleItImageField
from rentals.models import RentalProduct

# Create your models here.
class Van(RentalProduct):
	registration = models.CharField(max_length=10)
	odo = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	#Returns an array of unavailable days from today in format 'yyyy-mm-dd'
	def unavailable(self):
		return []


class VanPhotos(models.Model):
	def get_upload_path(instance, filename):
		return f'van_images/{self.van.slug}/{filename}'

	van = models.ForeignKey(Van, on_delete=models.CASCADE)
	photo = ScaleItImageField(max_width=1000, max_height=1000, quality=90, null=False, blank=False, upload_to=get_upload_path)
	banner = models.BooleanField(default=False)