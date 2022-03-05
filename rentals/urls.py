from django.urls import path, include

from .views import (
	MyRentals,
	RentalFulfilmentListView,
	RentalFulfilmentDetailView,
)

urlpatterns = [
	path('rentals/product/<slug:slug>/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('rentals/user/<int:pk>/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('rentals/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('rentals/my-rentals/<int:pk>/', MyRentals.as_view(), name='my-rentals'),
	path('rentals/my-rentals/', MyRentals.as_view(), name='my-rentals'),
    path('rentals/rental/price-check/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
	path('rentals/rental/price-check/<slug:slug>/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
	path('rentals/rental/<int:pk>/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
]
