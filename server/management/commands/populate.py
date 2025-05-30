import os
import random
import sys
import warnings

import markovify
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django_docopt_command import DocOptCommand
from model_bakery import baker

from accounts.models import Profile, User
from quotes.models import Quote, QuoteAuthor
from server.utils import model_data_customizer

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
                data = model_data_customizer("user", is_staff=arguments["--is-staff"])
                user_data = {"email": data["email"]}
                new_user = baker.make(User, **user_data)
                # refresh to avoid the signal side effect
                new_user.refresh_from_db()
                # add to the right group
                new_user.groups.add(Group.objects.get(name="Members"))

                print(
                    f"New member user created: {new_user.email} (Staff? {new_user.is_staff})"
                )

                # Also update the profile which was created via the signal
                new_user_prof = Profile.objects.get(user=new_user)
                new_user_prof.full_name = data["full_name"]
                new_user_prof.save()
                print(f"=> Profile for the user created: {new_user_prof.full_name}")
        elif arguments["--author"]:
            for _ in range(10):
                data = model_data_customizer("author")
                author_slug = data["name"].lower().replace(" ", "-")
                data["slug"] = author_slug
                new_author = baker.make(QuoteAuthor, **data)
                print(f"New author created: {new_author} {new_author.slug}")
