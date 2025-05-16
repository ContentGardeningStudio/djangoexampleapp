from faker import Faker
import random
from users.models import User

fake = Faker()


def get_users():
    return User.objects.filter(is_active=True, is_staff=True)


def quote_customizer():
    all_users = get_users()

    return {
        "quote": fake.sentence(nb_words=random.randint(6, 15)),
        "author": fake.name(),
        "poster": random.choice(all_users),
        "posted_date": fake.date_this_decade(),
    }


def user_customizer(is_staff=None):
    if is_staff is not None:
        return {"email": fake.email(), "is_staff": is_staff}
    return {"email": fake.email(), "is_staff": fake.boolean()}
