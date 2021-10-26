from django.contrib.auth.models import User
from django.db import models

from imageit.models import CropItImageField

# Create your models here.

class UserProfile(models.Model):
	def get_upload_path(instance, filename):
		return f'avatars/{instance.user.id}/{filename}'

	user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
	avatar = CropItImageField(max_width=300, max_height=300, quality=90, blank=True, null=True, upload_to=get_upload_path)


	def __str__(self):
		return self.user.email


	@property
	def display_name(self):
		if self.user.first_name != '' or self.user.last_name != '':
			return f'{self.user.first_name} {self.user.last_name}'
		else:
			return self.user.username


	@property
	def avatar_url(self):
		url = self.user.socialaccount_set.first().get_avatar_url()
		if self.avatar.name:
			return self.avatar.url
		elif url is not None:
			return url
		else:
			return ''