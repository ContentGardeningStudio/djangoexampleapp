from django_docopt_command import DocOptCommand
from quotes.models import Quote
from users.models import User
from model_bakery import baker
from faker import Faker
from quotes.lib import quote_customizer, user_customizer

import warnings

warnings.filterwarnings("ignore")

fake = Faker()


class Command(DocOptCommand):
    docs = """
        Populate database
        Usage:
            populate (-h | --help)
            populate (--quote)
            populate (--user)
        """

    def handle_docopt(self, arguments):
        if arguments["--quote"]:
            for _ in range(20):
                try:
                    new_quote = baker.make(Quote, **quote_customizer())
                    print(f"New quote created: {new_quote}")
                except Exception as e:
                    print("Exception: ", e)
        elif arguments["--user"]:
            for _ in range(20):
                try:
                    new_user = baker.make(User, **user_customizer())
                    print(f"New user created: {new_user}")
                except Exception as e:
                    print("Exception: ", e)
