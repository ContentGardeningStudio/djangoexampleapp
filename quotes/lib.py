from faker import Faker
import random
from users.models import User

fake = Faker()
all_user = User.objects.all()


def quote_customizer():
    return {
        "quote": fake.sentence(nb_words=random.randint(6, 15)),
        "author": fake.name(),
        "poster": random.choice(all_user),
        "posted_date": fake.date_this_decade(),
    }
