from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from allauth.account.views import EmailView
from allauth.socialaccount.views import ConnectionsView

from .forms import UserProfileUpdateForm, UserUpdateForm
from .models import UserProfile
# Create your views here.


class ProfileDetailView(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'accounts/profile_detail.html'
	success_url = reverse_lazy("profile")
	context_object_name = "usr"

	def get(self, *args, **kwargs):
		#If no user id is provided default to request.user
		if not self.kwargs.get('pk', False):
			self.kwargs['user_set'] = True
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)


def profile_update_view(request, pk, *args, **kwargs):
	user = User.objects.get(id=pk)
	if request.user.is_staff or user == request.user:
		if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=user)
			p_form = UserProfileUpdateForm(request.POST,
									   request.FILES,
									   instance=user.profile)
			if u_form.is_valid() and p_form.is_valid():
				u_form.save()
				p_form.save()
				messages.success(request, f'{ user.profile.display_name } has been updated!')
				#if request.is_ajax():
				#	return redirect(f'{ request.META.get("HTTP_REFERER") }?ajax=false')
				#return redirect(request.META.get('HTTP_REFERER'))
				return redirect(reverse_lazy('profile'))
		else:
			u_form = UserUpdateForm(instance=user)
			p_form = UserProfileUpdateForm(instance=user.profile)

		context = {
			'u_form': u_form,
			'p_form': p_form,
			'usr': user,
		}
		return render(request, 'accounts/profile_form.html', context)
	else:
		raise PermissionDenied


class ProfileConnectionsView(LoginRequiredMixin, ConnectionsView):
	template_name = 'accounts/profile_connections.html'

	def get(self, *args, **kwargs):
		#If no user id is provided default to request.user
		if not self.kwargs.get('pk', False):
			self.kwargs['user_set'] = True
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)
	
	def get_context_data(self, *args, **kwargs):
		ctx = super().get_context_data(*args, **kwargs)
		ctx.update({
			'usr': get_object_or_404(User, id=self.kwargs['pk'])
		})
		return ctx


class ProfileEmailView(LoginRequiredMixin, EmailView):
	template_name = 'accounts/profile_email.html'
	success_url = reverse_lazy("profile-email")

	def get(self, *args, **kwargs):
		#If no user id is provided default to request.user
		if not self.kwargs.get('pk', False):
			self.kwargs['user_set'] = True
			self.kwargs['pk'] = self.request.user.id
		return super().get(*args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		ctx = super().get_context_data(*args, **kwargs)
		ctx.update({
			'usr': get_object_or_404(User, id=self.kwargs['pk'])
		})
		return ctx