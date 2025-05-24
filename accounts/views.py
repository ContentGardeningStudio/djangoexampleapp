from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, View

from server.utils import SiteNavMixin

from .forms import ProfileForm, ProfileUpdateForm, UserRegisterForm
from .models import Profile


class RegisterView(SiteNavMixin, View):
    template_name = "account/register.html"
    success_url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "site_nav": self.get_site_nav(),
            },
        )

    def post(self, request, *args, **kwargs):
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile = user.profile
            profile.full_name = profile_form.cleaned_data["full_name"]
            profile.bio = profile_form.cleaned_data["bio"]
            profile.save(update_fields=["full_name", "bio"])
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect(self.success_url)
        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "site_nav": self.get_site_nav(),
            },
        )


class LoginView(SiteNavMixin, DjangoLoginView):
    template_name = "account/login.html"
    success_url = reverse_lazy("profile")


class LogoutView(DjangoLogoutView):
    next_page = "login"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You’ve been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class ProfileView(SiteNavMixin, LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"


class EditProfileView(SiteNavMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "account/edit_profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user.profile
