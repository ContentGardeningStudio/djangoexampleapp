from django_docopt_command import DocOptCommand

from quotes.models import Quote, QuoteAuthor


class Command(DocOptCommand):
    docs = """
            Clean database
            Usage:
                clean (-h | --help)
                clean --quote
                clean --author
            """

    def handle_docopt(self, arguments):
        if arguments["--quote"]:
            Quote.objects.all().delete()
            print("All Quotes has been deleted")
        elif arguments["--author"]:
            QuoteAuthor.objects.all().delete()
            print("All Authors has been deleted")
