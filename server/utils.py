from django_style import Nav


class SiteNavMixin:
    def get_site_nav(self):
        return [Nav("Home", "home"), Nav("Authors", "authors")]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_nav"] = self.get_site_nav()
        return context
