import os
from collections import namedtuple
from django import forms
from django.urls import reverse_lazy

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