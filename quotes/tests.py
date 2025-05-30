import pytest
from model_bakery import baker

from accounts.models import Profile, User

from .models import Quote, QuoteAuthor


@pytest.mark.django_db
def test_quote_create():
    my_user = baker.make(User, email="test@example.com", password="password123")
    profile = Profile.objects.get(user=my_user)
    author = baker.make(QuoteAuthor, name="John Doe")
    quote = baker.make(
        Quote, quote="This is a sample quote", poster=profile, author=author
    )
    assert str(quote) == "This is a sample quote - John Doe - By test@example.com"


@pytest.mark.django_db
def test_author_create():
    my_author = baker.make(QuoteAuthor, name="John Doe")
    assert my_author.name == "John Doe"


@pytest.mark.django_db
def test_author_slug():
    my_author = QuoteAuthor.objects.create(name="Jean Dupont")
    assert my_author.slug == "jean-dupont"
