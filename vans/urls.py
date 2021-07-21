from django.urls import path, include

from .views import (
	VanListView,
	VanDetailView,
)

urlpatterns = [
    path('', VanListView.as_view(), name='van-list'),
    path('<slug:slug>/', VanDetailView.as_view(), name='van-detail'),
]
