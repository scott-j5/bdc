from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from allauth.account.views import EmailView
from allauth.socialaccount.views import ConnectionsView

from .models import UserProfile
# Create your views here.


class ProfileDetail(LoginRequiredMixin, DetailView):
	model = UserProfile
	template_name = 'accounts/profile_detail.html'
	success_url = reverse_lazy("profile")

	def get(self, *args, **kwargs):
		if not self.kwargs.get('pk', False):
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)


class ProfileConnectionsView(LoginRequiredMixin, ConnectionsView):
	template_name = 'accounts/profile_connections.html'


class ProfileEmailView(LoginRequiredMixin, EmailView):
	template_name = 'accounts/profile_email.html'
	success_url = reverse_lazy("profile-email")