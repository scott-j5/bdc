from django.urls import path, include

from .views import (
    ProfileDetail
)

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile'),
	path('profile/', ProfileDetail.as_view(), name='profile'),
]
