from django.urls import path, include

from .views import (
	RentalFulfilmentListView,
	RentalFulfilmentDetailView,
)

urlpatterns = [
	path('rental-fulfilments/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
    path('rental-fulfilments/price-check/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
	path('rental-fulfilments/price-check/<slug:slug>/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
	path('rental-fulfilments/<int:pk>/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
]
