import pytest
from model_bakery import baker
from .models import Quote
from users.models import User


@pytest.mark.django_db
def test_quote_create():
    user = baker.make(User, email="test@example.com", password="password123")
    quote = baker.make(
        Quote, quote="This is a sample quote", poster=user, author="John Doe"
    )
    assert str(quote) == "This is a sample quote - John Doe - By test@example.com"
