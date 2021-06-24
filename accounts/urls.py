from django.urls import path, include

from core.views import (
    home_view
)

urlpatterns = [
    path('/profile/', home_view, name='profile'),
]
