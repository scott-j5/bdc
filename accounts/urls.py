from django.urls import path, include

from .views import (
    ProfileDetailView,
	profile_update_view,
	ProfileConnectionsView,
	ProfileEmailView
)

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
	path('profile/', ProfileDetailView.as_view(), name='profile'),
	path('profile/connections/', ProfileConnectionsView.as_view(), name='profile-connections'),
	path('profile/email/', ProfileEmailView.as_view(), name='profile-email'),

	path('profile/<int:pk>/edit/', profile_update_view, name='profile-update'),
]
