from allauth.account.views import LoginView, SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from server.utils import SiteNavMixin

from .forms import ProfileUpdateForm
from .models import Profile


class CustomSignupView(SiteNavMixin, SignupView):
    template_name = "account/signup.html"


class CustomLoginView(SiteNavMixin, LoginView):
    template_name = "account/login.html"
    success_url = reverse_lazy("profile")


class ProfileView(SiteNavMixin, LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"


class EditProfileView(SiteNavMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "account/edit_profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user.profile
