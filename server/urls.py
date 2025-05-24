from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts import views as accounts_views
from quotes import views as quotes_views

urlpatterns = (
    [
        path("", quotes_views.HomeView.as_view(), name="home"),
        path("authors", quotes_views.QuoteAuthorListView.as_view(), name="authors"),
        path(
            "author/<int:id>",
            quotes_views.QuoteAuthorDetailView.as_view(),
            name="author",
        ),
        path("admin/", admin.site.urls),
        path("register/", accounts_views.RegisterView.as_view(), name="register"),
        path("login/", accounts_views.LoginView.as_view(), name="login"),
        path("profile/", accounts_views.ProfileView.as_view(), name="profile"),
        path(
            "profile/edit/",
            accounts_views.EditProfileView.as_view(),
            name="edit_profile",
        ),
        path("logout/", accounts_views.LogoutView.as_view(), name="logout"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
)
