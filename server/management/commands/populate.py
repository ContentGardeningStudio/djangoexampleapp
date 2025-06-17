import os
import random
import sys
import warnings

import markovify
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.utils.text import slugify
from django_docopt_command import DocOptCommand
from faker import Faker
from model_bakery import baker

from accounts.models import Profile, User
from quotes.models import Quote, QuoteAuthor

# Optional: RAKE
try:
    import nltk
    from rake_nltk import Rake

    nltk.download("stopwords", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    USE_RAKE = True
except ImportError:
    USE_RAKE = False

warnings.filterwarnings("ignore")

fake = Faker()


# def get_active_users(only_staff=False):
#     if only_staff:
#         users = User.objects.filter(is_active=True, is_staff=True)
#     else:
#         users = User.objects.filter(is_active=True)
#     # print(users)
#     return Profile.objects.filter(user__in=users)


def model_data_customizer(model_name, **kwargs):
    match model_name:
        case "user":
            person = {
                "full_name": fake.name(),
                "email": fake.email(),
            }
            if "is_staff" in kwargs:
                person["is_staff"] = kwargs["is_staff"]
            else:
                person["is_staff"] = fake.boolean()
            return person
            # to do: handle the generation of the password?
        case "quote":
            users = User.objects.filter(is_active=True)
            profiles = Profile.objects.filter(user__in=users)
            authors = QuoteAuthor.objects.all()
            return {
                "quote": fake.sentence(nb_words=random.randint(6, 15)),
                "author": random.choice(authors),
                "poster": random.choice(profiles),
                "posted_date": fake.date_this_decade(),
            }
        case "author":
            return {"name": fake.name(), "country": fake.country_code()}
        case _:
            print("Not handled!")


class Command(DocOptCommand):
    docs = """
        Populate database
        Usage:
            populate (-h | --help)
            populate --quote
            populate --author
            populate --user [--is-staff]
        """

    def handle_docopt(self, arguments):
        if arguments["--quote"]:
            use_rake = USE_RAKE

            corpus_path = "data/inspirational_quotes.txt"
            if not os.path.exists(corpus_path):
                print(f"Missing corpus file (at {corpus_path})")
                sys.exit(1)

            with open(corpus_path, encoding="utf-8") as f:
                corpus = f.read()
            nlp_model = markovify.Text(corpus)

            # create quotes
            for _ in range(20):
                data = model_data_customizer("quote")
                # override the default quote text using the NLP model
                data["quote"] = nlp_model.make_short_sentence(140)
                try:
                    new_quote = baker.make(Quote, **data)
                except IntegrityError as e:
                    print(e)
                    new_quote = None

                if new_quote is not None:
                    text = new_quote.quote
                    if use_rake:
                        rake = Rake()
                        rake.extract_keywords_from_text(text)
                        tags = rake.get_ranked_phrases()[:3]
                    else:
                        # naïve approach
                        tags = []
                        split_text = text.split()
                        for _ in range(4):
                            random_word = random.choice(split_text)
                            tags.append(random_word)

                    # convert to lowercase
                    tags = [tag.lower() for tag in tags]
                    new_quote.tags.add(*tags)
                    print(
                        f"New quote created: {new_quote.quote}. Tags: {new_quote.tags.all()}"
                    )
        elif arguments["--user"]:
            # handles user + profile
            for _ in range(5):
                # print(arguments["--is-staff"])
                person_data = model_data_customizer(
                    "user", is_staff=arguments["--is-staff"]
                )

                # Rework the data needed for the user obj here
                user_data = person_data.copy()
                del user_data["full_name"]
                new_user = baker.make(User, **user_data)

                # refresh to avoid the signal side effect
                new_user.refresh_from_db()

                # set the password
                fake_password = fake.password(length=10)
                new_user.password = make_password(fake_password)
                new_user.save()

                # add to the right group
                new_user.groups.add(Group.objects.get(name="Members"))

                # Also update the profile which was created via the signal
                new_user_prof = Profile.objects.get(user=new_user)
                new_user_prof.full_name = person_data["full_name"]
                new_user_prof.save()

                msg = f"New member user created: {new_user.email} - password: {fake_password}"
                if new_user.is_staff:
                    msg = f"New STAFF member user created: {new_user.email} - password: {fake_password}"
                msg = msg + f" - Name: {new_user_prof.full_name}"
                print(msg)
        elif arguments["--author"]:
            for _ in range(10):
                data = model_data_customizer("author")
                data["slug"] = slugify(data["name"])
                new_author = baker.make(QuoteAuthor, **data)
                print(f"New author created: {new_author} {new_author.slug}")
