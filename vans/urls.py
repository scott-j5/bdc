from django.urls import path, include

from .views import (
    van_list,
	van_detail,
)

urlpatterns = [
    path('', van_list, name='van-list'),
    path('<slug:slug>/', van_detail, name='van-detail'),
]
