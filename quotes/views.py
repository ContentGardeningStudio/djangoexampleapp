from django.views.generic import DetailView, ListView
from django_style import Nav

from .models import Quote, QuoteAuthor


class CustomListView(ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CustomListView, self).get_context_data(**kwargs)

        # Create any data and add it to the context
        request = self.request
        site_nav = [Nav("Home", "home"), Nav("Authors", "list_authors")]
        if request.user.is_anonymous:
            site_nav += [Nav("Login", "login")]
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


class QuoteAuthorDetailView(DetailView):
    model = QuoteAuthor
    context_object_name = "author"
    template_name = "content/author.html"
    slug_field = "id"
    slug_url_kwarg = "id"
