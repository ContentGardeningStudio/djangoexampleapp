from django.core.paginator import Paginator
from django.shortcuts import render
from django_style import Nav

from .models import Quote


def list_quotes(request):
    quotes = Quote.objects.all().order_by("-posted_date").values()
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "quote/list_quotes.html",
        context={
            "site_nav": [
                Nav("Home", "list_quotes"),
                # Nav("Contact", "contact"),
            ],
            "page_obj": page_obj,
        },
    )


# def contact(request):
#     return HttpResponse("<h2>Contact</h2>")
