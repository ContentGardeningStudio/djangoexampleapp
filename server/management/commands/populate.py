import warnings

from django.contrib.auth.models import Group
from django_docopt_command import DocOptCommand
from model_bakery import baker

from quotes.models import Quote
from server.utils import model_data_customizer
from users.models import User

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
                    new_user.groups.add(Group.objects.get(name="Members"))

                    print(
                        f"New member user created: {new_user} (Staff? {new_user.is_staff})"
                    )
                except Exception as e:
                    print("Exception: ", e)
