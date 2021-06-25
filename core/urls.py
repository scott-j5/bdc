from django.urls import path, include

from .views import (
    home_view,
	vans_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
	path('vans/', home_view, name='vans-list'),
]
