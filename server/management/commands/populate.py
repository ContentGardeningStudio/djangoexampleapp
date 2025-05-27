import random
import warnings

from django.contrib.auth.models import Group
from django_docopt_command import DocOptCommand
from model_bakery import baker

from accounts.models import Profile, User
from quotes.models import Quote, QuoteAuthor
from server.utils import model_data_customizer

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
            for _ in range(20):
                data = model_data_customizer("quote")
                new_quote = baker.make(Quote, **data)
                print(new_quote.quote.split())
                for _ in range(3):
                    split_quote = new_quote.quote.split()
                    random_word_in_split_quote = random.choice(split_quote)
                    new_quote.tags.add(random_word_in_split_quote)
                print(f"New quote created: {new_quote}")
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
            for _ in range(20):
                data = model_data_customizer("author")
                new_author = baker.make(QuoteAuthor, **data)
                print(f"New author created: {new_author}")
