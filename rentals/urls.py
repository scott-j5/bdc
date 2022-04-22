from django.urls import path, include

from .views import (
	MyRentals,
	RentalFulfilmentListView,
	RentalFulfilmentDetailView,
	RentalFulfilmentPriceCheckView,

	RentalFulfilmentCreateView,
	RentalFulfilmentConfirmExtras,
	RentalFulfilmentConfirmExtraInformation,
	RentalFulfilmentConfirmDrivers,
	RentalFulfilmentDriverCreateView,
	RentalFulfilmentDriverUpdateView,
	RentalFulfilmentTerms
)

urlpatterns = [
	path('list/product/<slug:slug>/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('list/user/<int:pk>/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	path('list/', RentalFulfilmentListView.as_view(), name='rental-fulfilment-list'),
	
	path('my-rentals/user/<int:pk>/', MyRentals.as_view(), name='my-rentals'),
	path('my-rentals/', MyRentals.as_view(), name='my-rentals'),

	path('rental/<int:pk>/', RentalFulfilmentDetailView.as_view(), name='rental-fulfilment-detail'),

    path('rental/price-check/', RentalFulfilmentPriceCheckView.as_view(), name='rental-fulfilment-price-check'),
	path('rental/price-check/product/<slug:slug>/', RentalFulfilmentPriceCheckView.as_view(), name='rental-fulfilment-price-check'),
	path('rental/price-check/<int:pk>/', RentalFulfilmentPriceCheckView.as_view(), name='rental-fulfilment-price-check'),

	path('terms/', RentalFulfilmentTerms.as_view(), name='rental-fulfilment-terms'),
	path('rental/add/', RentalFulfilmentCreateView.as_view(), name='rental-fulfilment-add'),
	path('rental/<int:pk>/extra-information/', RentalFulfilmentConfirmExtraInformation.as_view(), name='rental-fulfilment-extra-information'),
	path('rental/<int:pk>/extras/', RentalFulfilmentConfirmExtras.as_view(), name='rental-fulfilment-extras'),
	path('rental/<int:pk>/drivers/', RentalFulfilmentConfirmDrivers.as_view(), name='rental-fulfilment-drivers'),
	path('rental/<int:rental_pk>/drivers/add/', RentalFulfilmentDriverCreateView.as_view(), name='rental-fulfilment-driver-add'),
	path('rental/<int:rental_pk>/drivers/<int:pk>/update/', RentalFulfilmentDriverUpdateView.as_view(), name='rental-fulfilment-driver-update'),
]
