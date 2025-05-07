import pytest
from model_bakery import baker
from .models import Quote
from users.models import User
from datetime import datetime


@pytest.mark.django_db
def test_quote_create():
    # user = User.objects.first()
    # user = create_user()
    user = baker.make(User, email="test@example.com", password="password123")
    quote = baker.make(Quote, quote="quote", posted_date=datetime.now(), poster=user)
    assert str(quote) == "quote"