import pytest
from model_bakery import baker

from users.models import Profile, User

from .models import Quote


@pytest.mark.django_db
def test_quote_create():
    my_user = baker.make(User, email="test@example.com", password="password123")
    # profile = baker.make(Profile, user=user)
    profile = Profile.objects.get(user=my_user)
    quote = baker.make(
        Quote, quote="This is a sample quote", poster=profile, author="John Doe"
    )
    # print(str(quote))
    # print("This is a sample quote - John Doe - By test@example.com")
    assert str(quote) == "This is a sample quote - John Doe - By test@example.com"
