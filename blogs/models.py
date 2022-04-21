from django.db import models

# Create your models here.
import math

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from djrichtextfield.models import RichTextField

from imageit.models import ScaleItImageField, CropItImageField

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(unique=True, max_length=100, default=1)

	def __str__(self):
		return f'{self.name}'


class Series(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=150)


class Blog(models.Model):
	def get_upload_path(instance, filename):
		return f'blog_images/{instance.slug}/{filename}'

	author = models.ForeignKey(User, on_delete=models.PROTECT)
	published = models.BooleanField(default=False)
	published_on = models.DateTimeField(default=None, null=True, blank=True)
	updated = models.DateTimeField(default=timezone.now, null=False, blank=False)
	title = models.CharField(max_length=150)
	slug = models.SlugField(max_length=150, unique=True, null=False, blank=True, help_text='Leave blank to auto-generate')
	description = models.CharField(max_length=500)
	thumbnail = ScaleItImageField(max_width=250, max_height=250, quality=100, null=True, blank=True, upload_to=get_upload_path)
	banner = CropItImageField(max_width=1000, max_height=1000, null=True, blank=True, upload_to=get_upload_path)
	views = models.IntegerField(default=0)
	series = models.ForeignKey(Series, on_delete=models.SET_NULL, blank=True, null=True)
	tags = models.ManyToManyField(Tag)
	content = RichTextField(default='')

	@property
	def author_name(self):
		return f'{self.author.first_name} {self.author.last_name}' if self.author.first_name else self.author.username

	@property
	def read_time(self):
		return math.ceil(len(str(self.content).split()) / 225)

	def __str__(self):
		return f'{self.title}' if self.published else f'(DRAFT) - {self.title}'

	@staticmethod
	def dict_filter(filter_dict):
		filters = {}
		if filter_dict.get('id'):
			filters['id'] = filter_dict['id']
		if filter_dict.get('search'):
			filters['title__icontains'] = filter_dict['search']
		result = Blog.objects.filter(**filters)
		if filter_dict.get('tags'):
			for tag in filter_dict.get('tags'):
				result = result.filter(tags__slug=tag)
		return result
	
	def clean(self, *args, **kwargs):
		if self.slug == '' or self.slug == None:
			self.slug = self.title.replace(' ', '-').lower()
		super().clean(*args, **kwargs)

	def increment_views(self):
		self.views = self.views + 1
		self.save(updated=False)

	def save(self, *args, **kwargs):
		is_published = Blog.objects.only("published").filter(id=self.id).first()

		if kwargs.pop("updated", True) != False:
			self.updated = timezone.now()

		if is_published and not is_published.published and self.published:
			self.published_on = timezone.now()
		super().save(*args, **kwargs)

	class Meta:
		ordering = ['-published_on', 'title']


class BlogImage(models.Model):
    def get_upload_path(instance, filename):
        return f'blog_images/{instance.blog.slug}/content/{filename}'

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    image = ScaleItImageField(max_width=1000, max_height=1000, null=False, blank=False, upload_to=get_upload_path)

    def __str__(self):
        return f'{self.image.name}'
