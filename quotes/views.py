from django.views.generic import DetailView, ListView

from server.utils import SiteNavMixin

from .models import Quote, QuoteAuthor


class HomeView(SiteNavMixin, ListView):
    # queryset = Quote.objects.all().order_by("-posted_date")
    queryset = Quote.objects.prefetch_related("author").all()
    context_object_name = "quotes"
    template_name = "content/home.html"
    paginate_by = 10


class QuoteAuthorListView(SiteNavMixin, ListView):
    queryset = QuoteAuthor.objects.all().order_by("-name")
    context_object_name = "authors"
    template_name = "content/authors.html"
    paginate_by = 10


class QuoteAuthorDetailView(SiteNavMixin, DetailView):
    model = QuoteAuthor
    context_object_name = "author"
    template_name = "content/author.html"
    slug_field = "id"
    slug_url_kwarg = "id"
