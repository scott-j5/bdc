from django.urls import path, include

from .views import (
	VanDetailView,
	VanListView,
    van_list,
	van_detail,
)

urlpatterns = [
    path('', van_list, name='van-list'),
    path('<slug:slug>/', VanDetailView.as_view(), name='van-detail'),
]
