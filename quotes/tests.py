import pytest
from model_bakery import baker

from accounts.models import Profile, User

from .models import Quote, QuoteAuthor


@pytest.mark.django_db
def test_quote_create():
    my_user = baker.make(User, email="test@example.com", password="password123")
    # profile = baker.make(Profile, user=user)
    profile = Profile.objects.get(user=my_user)
    author = baker.make(QuoteAuthor, name="John Doe")
    quote = baker.make(
        Quote, quote="This is a sample quote", poster=profile, author=author
    )
    # print(str(quote))
    # print("This is a sample quote - John Doe - By test@example.com")
    assert str(quote) == "This is a sample quote - John Doe - By test@example.com"


@pytest.mark.django_db
def test_author_create():
    my_author = baker.make(QuoteAuthor, name="John Doe")
    assert str(my_author) == "John Doe"


@pytest.mark.django_db
def test_author_slug():
    my_author = baker.make(QuoteAuthor, name="Jean Dupont")
    assert str(my_author.slug) == "jean-dupont"
