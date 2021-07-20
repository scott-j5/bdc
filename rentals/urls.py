from django.urls import path, include

from .views import (
	RentalDetailView
)

urlpatterns = [
    path('', van_list, name='van-list'),
    path('<int:pk>/', RentalDetailView.as_view(), name='product-rental-detail'),
]
