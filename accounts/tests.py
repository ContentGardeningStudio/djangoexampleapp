import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from accounts.models import Profile, User


@pytest.mark.django_db
def test_user_create():
    user = baker.make(User, email="test@example.com", password="password123")
    assert user.email == "test@example.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_superuser_create():
    superuser = User.objects.create_superuser(
        email="admin@example.com", password="admin123"
    )
    assert superuser.email == "admin@example.com"
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser
    assert str(superuser) == "admin@example.com"


@pytest.mark.django_db
def test_profile_created():
    user = baker.make(User, email="test@example.com", password="password123")
    # profile has been created because of the signal
    profile = Profile.objects.get(user=user)
    assert str(profile) == "test@example.com"
    assert profile.user.email == "test@example.com"
    # we can update the profile
    image = SimpleUploadedFile("test_image.jpg", content=b"", content_type="image/jpeg")
    profile.picture = image
    profile.bio = "Test Bio"
    profile.save()
    # assert profile.picture.url.startswith("/profile_pics/test_image_")
    assert profile.bio == "Test Bio"
