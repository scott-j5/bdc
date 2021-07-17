from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Reservation(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
	check_in = models.DateTimeField()
	check_out = models.DateTimeField()

	def length_days(self):
		return abs((self.check_out - self.check_in).days)