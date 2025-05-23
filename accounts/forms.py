from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
            )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
            )

    class Meta:
        model = Profile
        fields = ("full_name", "bio")  # adjust fields as needed


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "bio", "picture"]

        widgets = {
            "picture": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 \
                          file:rounded-full file:border-0 file:text-sm file:font-semibold \
                          file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                }
            )
        }
