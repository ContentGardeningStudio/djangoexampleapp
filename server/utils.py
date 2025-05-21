import random

from faker import Faker

from quotes.models import QuoteAuthor
from users.models import Profile, User

fake = Faker()


def get_active_users(only_staff=True):
    if only_staff:
        staff_users = User.objects.filter(is_active=True, is_staff=True)
        return Profile.objects.filter(user__in=staff_users)
    active = User.objects.filter(is_active=True)
    return Profile.objects.filter(user__in=active)


def model_data_customizer(model_name, **kwargs):
    match model_name:
        case "user":
            if "is_staff" in kwargs:
                return {"email": fake.email(), "is_staff": kwargs["is_staff"]}
            return {"email": fake.email(), "is_staff": fake.boolean()}
            # to do: handle the generation of the password?
        case "quote":
            staff_users = get_active_users(only_staff=True)
            authors = QuoteAuthor.objects.all()
            return {
                "quote": fake.sentence(nb_words=random.randint(6, 15)),
                "author": random.choice(authors),
                "poster": random.choice(staff_users),
                "posted_date": fake.date_this_decade(),
            }
        case "author":
            return {
                "name": fake.name(),
            }
        case _:
            print("Not handled!")
