from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView
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
        "content/home.html",
        context={
            "site_nav": site_nav,
            "page_obj": page_obj,
        },
    )


# def list_authors(request):
#     authors = QuoteAuthor.objects.all()
#     paginator = Paginator(authors, 10)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     site_nav = [Nav("Home", "home"), Nav("Authors", "list_authors")]
#     if request.user.is_anonymous:
#         site_nav += [Nav("Login", "login"), Nav("Register", "register")]
#     else:
#         site_nav += [Nav("Profile", "profile"), Nav("Logout", "logout")]
#
#     return render(
#         request,
#         "content/authors.html",
#         context={
#             "site_nav": site_nav,
#             "page_obj": page_obj,
#         },
#     )


class QuoteAuthorListView(ListView):
    model = QuoteAuthor
    queryset = QuoteAuthor.objects.all()
    context_object_name = "authors"
    template_name = "content/authors.html"
