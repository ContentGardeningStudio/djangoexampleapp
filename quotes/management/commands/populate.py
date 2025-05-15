from django_docopt_command import DocOptCommand
from quotes.models import Quote
from model_bakery import baker
from faker import Faker
from quotes.lib import quote_customizer

import warnings
warnings.filterwarnings('ignore')

fake = Faker()


class Command(DocOptCommand):
    docs = """
        Populate database
        Usage:
            populate (-h | --help)
            populate
        """

    def handle_docopt(self, arguments):
        for _ in range(1000):
            try:
                baker.make(Quote, **quote_customizer())
            except Exception as e:
                print("Exception: ", e)
