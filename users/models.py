from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        hashed_password = make_password(password=password)
        user.set_password(hashed_password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


# Custom User
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    # password2 = forms.CharField(
    #     label="Password confirmation", widget=forms.PasswordInput
    # )

    class Meta:
        model = User
        fields = ["email"]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "is_staff"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "is_staff"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_staff"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {"classes": ["wide"], "fields": ["email", "password"]},
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_pics/")
    bio = models.TextField()

    def __str__(self):
        return f"{self.user} profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
