from django.db import models
from imageit.models import ScaleItImageField
from rentals.models import RentalProduct

# Create your models here.
class Van(RentalProduct):
	DRIVE_CHOICES = [("4x4", "4x4"),("2x4", "2x4")]
	make = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	sleeps = models.IntegerField()
	seats = models.IntegerField()
	drive_type = models.CharField(max_length=3, blank=False, null=False, choices=DRIVE_CHOICES)
	pets = models.BooleanField(default=True)
	registration = models.CharField(max_length=10)
	odo = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class VanPhotos(models.Model):
	def get_upload_path(instance, filename):
		return f'van_images/{self.van.slug}/{filename}'

	van = models.ForeignKey(Van, on_delete=models.CASCADE)
	photo = ScaleItImageField(max_width=1000, max_height=1000, quality=90, null=False, blank=False, upload_to=get_upload_path)
	banner = models.BooleanField(default=False)