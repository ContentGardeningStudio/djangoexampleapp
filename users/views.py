from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django_style import Nav

from .forms import ProfileForm, UserRegisterForm
from .models import Profile


def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            print(user.__dict__)
            # profile has been created because of the signal
            profile = Profile.objects.get(user=user)
            profile.full_name = profile_form.cleaned_data["full_name"]
            profile.bio = profile_form.cleaned_data["bio"]
            profile.save()
            return redirect("list_quotes")
            # login(request, user)
            # return redirect('profile')  # or any other page
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(
        request,
        "user/register.html",
        context={
            "site_nav": [
                Nav("Home", "list_quotes"),
            ],
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})
