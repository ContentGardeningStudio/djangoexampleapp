from django.views.generic import DetailView, ListView

from server.utils import SiteNavMixin

from .models import Quote, QuoteAuthor


class HomeView(SiteNavMixin, ListView):
    queryset = (
        Quote.objects.select_related("author", "poster")
        .prefetch_related("tags")
        .order_by("-posted_date")
    )
    # context_object_name = "quotes"  # not needed, we use page_obj since we have pagination
    template_name = "content/home.html"
    paginate_by = 10


class QuoteAuthorListView(SiteNavMixin, ListView):
    queryset = QuoteAuthor.objects.all().order_by("-name")
    # context_object_name = "authors"
    template_name = "content/authors.html"
    paginate_by = 10


class QuoteAuthorDetailView(SiteNavMixin, DetailView):
    model = QuoteAuthor
    context_object_name = "author"
    template_name = "content/author.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        context["object_list"] = (
            Quote.objects.select_related("author", "poster")
            .prefetch_related("tags")
            .filter(author=author)
            .order_by("-posted_date")
        )
        return context
