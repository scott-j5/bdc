from django.urls import path, include

from .views import (
    ProfileDetail,
	ProfileConnectionsView,
	ProfileEmailView
)

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile'),
	path('profile/', ProfileDetail.as_view(), name='profile'),
	path('profile/connections/', ProfileConnectionsView.as_view(), name='profile-connections'),
	path('profile/email/', ProfileEmailView.as_view(), name='profile-email'),

	path('profile/edit/', ProfileDetail.as_view(), name='profile-update'),
]
