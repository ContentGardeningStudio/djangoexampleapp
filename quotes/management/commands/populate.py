from django_docopt_command import DocOptCommand
from quotes.models import Quote
from users.models import User
from model_bakery import baker

# from faker import Faker
from quotes.lib import quote_customizer, user_customizer

import warnings

warnings.filterwarnings("ignore")


class Command(DocOptCommand):
    docs = """
        Populate database
        Usage:
            populate (-h | --help)
            populate (--quote)
            populate (--user <is_staff>)
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
            is_staff_argument = (
                arguments["<is_staff>"] if arguments["<is_staff>"] else None
            )
            # if is_staff_argument is None, random boolean will be used
            for _ in range(5):
                try:
                    new_user = baker.make(
                        User, **user_customizer(is_staff=is_staff_argument)
                    )
                    print(f"New user created: {new_user} {new_user.is_staff}")
                except Exception as e:
                    print("Exception: ", e)
