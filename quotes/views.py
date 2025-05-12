from .models import Quote
from django.shortcuts import render
from django_style import Nav
from django.http import HttpResponse


def list_quotes(request):
    return render(
        request,
        "quote/list_quotes.html",
        context={
            "site_nav": [
                Nav("Home", "list_quotes"),
                Nav("Contact", "contact"),
            ],
            "quotes": Quote.objects.all(),
        },
    )


def contact(request):
    return HttpResponse("<h2>Contact</h2>")
