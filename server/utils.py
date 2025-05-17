import random

from faker import Faker

from users.models import User

fake = Faker()


def get_active_users(only_staff=True):
    if only_staff:
        return User.objects.filter(is_active=True, is_staff=True)
    return User.objects.filter(is_active=True)


def model_data_customizer(model_name, **kwargs):
    match model_name:
        case "user":
            if "is_staff" in kwargs:
                return {"email": fake.email(), "is_staff": kwargs["is_staff"]}
            return {"email": fake.email(), "is_staff": fake.boolean()}
            # to do: handle the generation of the password?
        case "quote":
            staff_users = get_active_users(only_staff=True)
            return {
                "quote": fake.sentence(nb_words=random.randint(6, 15)),
                "author": fake.name(),
                "poster": random.choice(staff_users),
                "posted_date": fake.date_this_decade(),
            }
        case _:
            print("Not handled!")
