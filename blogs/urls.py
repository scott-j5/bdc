from django.contrib import admin
from django.urls import path

from .views import blog_list, BlogDetail, BlogImageUpload, blog_image

urlpatterns = [
    path('', blog_list, name='blog-list'),
    path('blog/<slug:slug>/', BlogDetail.as_view(), name='blog-detail'),
    path('blog/<slug:blog>/image/upload/', BlogImageUpload.as_view(), name='blog-image-upload'),
    path('blog/image/<int:pk>/', blog_image, name='blog-image'),
]
