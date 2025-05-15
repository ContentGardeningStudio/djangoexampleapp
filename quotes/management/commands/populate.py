from django_docopt_command import DocOptCommand
from quotes.models import Quote
from users.models import User
import random
from faker import Faker

fake = Faker()


class Command(DocOptCommand):
    docs = """
        Populate database
        Usage:
            populate (-h | --help)
            populate <nb_quotes>
        """

    def handle_docopt(self, arguments):
        nb_quotes = int(arguments["<nb_quotes>"])
        user = User.objects.get(id=1)

        for _ in range(0, nb_quotes):
            new_quote = Quote(
                quote=fake.sentence(nb_words=random.randint(6, 15)),
                author=fake.name(),
                posted_date=fake.date_this_decade(),
                poster=user,
            )
            new_quote.save()
