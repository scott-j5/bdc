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
	context_object_name = "base_user"

	def get(self, *args, **kwargs):
		#If no user id is provided default to request.user
		if not self.kwargs.get('pk', False):
			self.kwargs['user_set'] = True
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)


class ProfileConnectionsView(LoginRequiredMixin, ConnectionsView):
	template_name = 'accounts/profile_connections.html'

	def get(self, *args, **kwargs):
		#If no user id is provided default to request.user
		if not self.kwargs.get('pk', False):
			self.kwargs['user_set'] = True
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)


class ProfileEmailView(LoginRequiredMixin, EmailView):
	template_name = 'accounts/profile_email.html'
	success_url = reverse_lazy("profile-email")

	def get(self, *args, **kwargs):
		#If no user id is provided default to request.user
		if not self.kwargs.get('pk', False):
			self.kwargs['user_set'] = True
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)