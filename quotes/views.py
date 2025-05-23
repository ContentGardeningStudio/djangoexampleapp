from django.views.generic import ListView
from django_style import Nav

from .models import Quote, QuoteAuthor

# def home(request):
#     quotes = Quote.objects.all().order_by("-posted_date")
#     paginator = Paginator(quotes, 10)
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
#         "content/home.html",
#         context={
#             "site_nav": site_nav,
#             "page_obj": page_obj,
#         },
#     )


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


class CustomListView(ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CustomListView, self).get_context_data(**kwargs)

        # Create any data and add it to the context
        request = self.request
        site_nav = [Nav("Home", "home"), Nav("Authors", "list_authors")]
        if request.user.is_anonymous:
            site_nav += [Nav("Login", "login"), Nav("Register", "register")]
        else:
            site_nav += [Nav("Profile", "profile"), Nav("Logout", "logout")]

        context["site_nav"] = site_nav
        return context


class QuoteAuthorListView(CustomListView):
    queryset = QuoteAuthor.objects.all().order_by("-name")
    context_object_name = "authors"
    template_name = "content/authors.html"
    paginate_by = 10


class HomeView(CustomListView):
    queryset = Quote.objects.all().order_by("-posted_date")
    context_object_name = "quotes"
    template_name = "content/home.html"
    paginate_by = 10
