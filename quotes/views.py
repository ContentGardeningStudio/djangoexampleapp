from django.core.paginator import Paginator
from django.shortcuts import render
from django_style import Nav

from .models import Quote, QuoteAuthor


def home(request):
    quotes = Quote.objects.all().order_by("-posted_date")
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    site_nav = [Nav("Home", "home"), Nav("Authors", "list_authors")]
    if request.user.is_anonymous:
        site_nav += [Nav("Login", "login"), Nav("Register", "register")]
    else:
        site_nav += [Nav("Profile", "profile"), Nav("Logout", "logout")]

    return render(
        request,
        "home.html",
        context={
            "site_nav": site_nav,
            "page_obj": page_obj,
        },
    )


def list_authors(request):
    authors = QuoteAuthor.objects.all()
    paginator = Paginator(authors, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    site_nav = [Nav("Home", "home"), Nav("Authors", "list_authors")]
    if request.user.is_anonymous:
        site_nav += [Nav("Login", "login"), Nav("Register", "register")]
    else:
        site_nav += [Nav("Profile", "profile"), Nav("Logout", "logout")]

    return render(
        request,
        "authors.html",
        context={
            "site_nav": site_nav,
            "page_obj": page_obj,
        },
    )


# def contact(request):
#     return HttpResponse("<h2>Contact</h2>")
