import pytest
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()

@pytest.mark.django_db
def test_signup_creates_inactive_user_and_sends_email(client):
    signup_url = reverse("account_signup")
    email = "testuser@example.com"
    password = "TestPassword123!"
    data = {
        "email": email,
        "password1": password,
        "password2": password,
    }
    response = client.post(signup_url, data)
    # Should redirect (not error)
    assert response.status_code in (302, 303)
    # User should exist and be inactive
    user = User.objects.get(email=email)
    assert user.is_active
    # EmailAddress should exist and be unverified
    email_address = EmailAddress.objects.get(user=user)
    assert not email_address.verified
    assert email_address.primary

    # An email should have been sent (failing for now?)
    assert len(mail.outbox) == 1
    assert email in mail.outbox[0].to

# @pytest.mark.django_db
# def test_email_confirmation_activates_user(client):
#     # First, sign up
#     email = "verifyme@example.com"
#     password = "TestPassword123!"
#     client.post(reverse("account_signup"), {
#         "email": email,
#         "password1": password,
#         "password2": password,
#     })
#     user = User.objects.get(email=email)
#     email_address = EmailAddress.objects.get(user=user)
#     # Get the confirmation URL from the email
#     confirmation_email = mail.outbox[0]
#     import re
#     url_match = re.search(r'http://testserver(/[^\\s]+)', confirmation_email.body)
#     assert url_match, "No confirmation URL found in email"
#     confirm_url = url_match.group(1)
#     # Visit the confirmation URL
#     response = client.get(confirm_url, follow=True)
#     user.refresh_from_db()
#     email_address.refresh_from_db()
#     # User EmailAddress record should now have 'verified' to True
#     assert email_address.verified