from django.urls import path, include

from .views import (
	MyRentals,
	RentalFulfilmentListView,
	RentalFulfilmentDetailView,

	RentalFulfilmentCreateView,
	RentalFulfilmentConfirmExtras,
	RentalFulfilmentConfirmDetails,
)

urlpatterns = [
	path('list/product/<slug:slug>/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('list/user/<int:pk>/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('list/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('my-rentals/user/<int:pk>/', MyRentals.as_view(), name='my-rentals'),
	path('my-rentals/', MyRentals.as_view(), name='my-rentals'),
    path('rental/price-check/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
	path('rental/price-check/<slug:slug>/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),
	path('rental/<int:pk>/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),

	path('rental/add/', RentalFulfilmentCreateView.as_view(), name='rental-fulfilment-add'),
	path('rental/<int:pk>/extras/', RentalFulfilmentConfirmExtras.as_view(), name='rental-fulfilment-extras'),
	path('rental/<int:pk>/details/', RentalFulfilmentConfirmDetails.as_view(), name='rental-fulfilment-details'),
]
