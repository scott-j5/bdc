from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from .models import UserProfile
# Create your views here.


class ProfileDetail(LoginRequiredMixin, DetailView):
	model = UserProfile
	template_name = 'accounts/profile_detail.html'

	def get(self, *args, **kwargs):
		if not self.kwargs.get('pk', False):
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)
