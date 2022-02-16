from django.urls import path, include

from .views import (
	VanListView,
	VanDetailView,
	VanUpdateView,
	VanDeleteView,
)

urlpatterns = [
    path('', VanListView.as_view(), name='van-list'),
    path('<slug:slug>/', VanDetailView.as_view(), name='van-detail'),
	path('<slug:slug>/update/', VanUpdateView.as_view(), name='van-update'),
	path('<slug:slug>/delete/', VanDeleteView.as_view(), name='van-delete'),
]
