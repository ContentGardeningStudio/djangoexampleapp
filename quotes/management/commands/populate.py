from django_docopt_command import DocOptCommand
from quotes.models import Quote
from model_bakery import baker
from faker import Faker
from quotes.lib import quote_customizer

fake = Faker()


class Command(DocOptCommand):
    docs = """
        Populate database
        Usage:
            populate (-h | --help)
            populate
        """

    def handle_docopt(self, arguments):
        for _ in range(20):
            try:
                new_quote = baker.make(Quote, **quote_customizer())
                print(f"New quote created: {new_quote}")
            except Exception as e:
                print("Exception: ", e)
