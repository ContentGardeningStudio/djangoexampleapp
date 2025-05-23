import random

from faker import Faker

from accounts.models import Profile, User
from quotes.models import QuoteAuthor

fake = Faker()


def get_active_users(only_staff=False):
    if only_staff:
        users = User.objects.filter(is_active=True, is_staff=True)
    else:
        users = User.objects.filter(is_active=True)
    print(users)
    return Profile.objects.filter(user__in=users)


def model_data_customizer(model_name, **kwargs):
    match model_name:
        case "user":
            person = {"full_name": fake.name(), "email": fake.email()}
            if "is_staff" in kwargs:
                person["is_staff"] = kwargs["is_staff"]
            else:
                person["is_staff"] = fake.boolean()
            return person
            # to do: handle the generation of the password?
        case "quote":
            active_users = get_active_users()
            authors = QuoteAuthor.objects.all()
            return {
                "quote": fake.sentence(nb_words=random.randint(6, 15)),
                "author": random.choice(authors),
                "poster": random.choice(active_users),
                "posted_date": fake.date_this_decade(),
            }
        case "author":
            return {
                "name": fake.name(),
            }
        case _:
            print("Not handled!")
