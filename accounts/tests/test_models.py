import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from accounts.models import Profile, User


@pytest.mark.django_db
def test_create_user():
    user = baker.make(User, email="test@example.com", password="password123", is_active=True)
    assert user.email == "test@example.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(
        email="admin@example.com", password="admin123"
    )
    assert superuser.email == "admin@example.com"
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser
    assert str(superuser) == "admin@example.com"


@pytest.mark.django_db
def test_create_profile():
    user = baker.make(User, email="test@example.com", password="password123", is_active=True)
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


@pytest.mark.django_db
def test_create_user_defaults():
    user = User.objects.create_user(email="test2@example.com", password="password123")
    assert user.email == "test2@example.com"
    assert user.is_active  # Should be True by default
    assert not user.email_verified  # Should be False by default

@pytest.mark.django_db
def test_email_verification_signal():
    user = User.objects.create_user(email="verifyme@example.com", password="password123")
    from allauth.account.signals import email_confirmed
    from django.dispatch import Signal
    # Simulate email confirmation
    class DummyEmailAddress:
        def __init__(self, user):
            self.user = user
    email_address = DummyEmailAddress(user)
    email_confirmed.send(sender=None, request=None, email_address=email_address)
    user.refresh_from_db()
    assert user.email_verified
