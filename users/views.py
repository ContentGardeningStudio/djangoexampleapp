from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django_style import Nav

from .forms import ProfileForm, UserRegisterForm
from .models import Profile

default_nav = [
    Nav("Home", "home"),
]


def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # here, profile should have been created because of the signal
            # but, force the signal side effect to be fully available
            user.refresh_from_db()
            profile = Profile.objects.get(user=user)
            profile.full_name = profile_form.cleaned_data["full_name"]
            profile.bio = profile_form.cleaned_data["bio"]
            profile.save(update_fields=["full_name", "bio"])
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("profile")
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    site_nav = [Nav("Home", "home"), Nav("Login", "login")]

    return render(
        request,
        "user/register.html",
        context={
            "site_nav": site_nav,
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm()

    site_nav = [Nav("Home", "home"), Nav("Register", "register")]

    return render(
        request,
        "user/login.html",
        context={
            "site_nav": site_nav,
            "form": form,
        },
    )


@login_required
def profile_view(request):
    site_nav = [Nav("Home", "home"), Nav("Logout", "logout")]

    return render(
        request,
        "user/profile.html",
        context={
            "site_nav": site_nav,
            "user": request.user,
            "profile": request.user.profile,
        },
    )


def custom_logout_view(request):
    logout(request)
    messages.success(request, "You’ve been logged out successfully.")
    return redirect("login")
