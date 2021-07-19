from django.urls import path, include

from .views import (
	VanListView,
	VanDetailView,
    van_list,
)

urlpatterns = [
    path('', van_list, name='van-list'),
    path('<slug:slug>/', VanDetailView.as_view(), name='van-detail'),
]
