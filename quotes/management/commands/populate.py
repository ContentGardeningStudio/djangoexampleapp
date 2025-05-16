from django_docopt_command import DocOptCommand
from quotes.models import Quote
from users.models import User
from model_bakery import baker

from quotes.lib import model_data_customizer

import warnings

warnings.filterwarnings("ignore")


class Command(DocOptCommand):
    docs = """
        Populate database
        Usage:
            populate (-h | --help)
            populate --quote
            populate --user [--is-staff]
        """

    def handle_docopt(self, arguments):
        if arguments["--quote"]:
            for _ in range(20):
                try:
                    data = model_data_customizer("quote")
                    new_quote = baker.make(Quote, **data)
                    print(f"New quote created: {new_quote}")
                except Exception as e:
                    print("Exception: ", e)
        elif arguments["--user"]:
            for _ in range(5):
                try:
                    data = model_data_customizer(
                        "user", is_staff=arguments["--is-staff"]
                    )
                    new_user = baker.make(User, **data)
                    print(f"New user created: {new_user} (Staff? {new_user.is_staff})")
                except Exception as e:
                    print("Exception: ", e)
