from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views as accounts_views
from quotes import views as quotes_views

urlpatterns = [
    path("", quotes_views.HomeView.as_view(), name="home"),
    path("authors", quotes_views.QuoteAuthorListView.as_view(), name="authors"),
    path(
        "author/<int:id>",
        quotes_views.QuoteAuthorDetailView.as_view(),
        name="author",
    ),
    path("admin/", admin.site.urls),
    path("accounts/signup/", accounts_views.CustomSignupView.as_view(), name="signup"),
    path(
        "accounts/login/",
        accounts_views.CustomLoginView.as_view(),
        name="account_login",
    ),
    path("accounts/", include("allauth.urls")),  # enables social + email login
    path("profile/", accounts_views.ProfileView.as_view(), name="profile"),
    path(
        "profile/edit/",
        accounts_views.EditProfileView.as_view(),
        name="edit_profile",
    ),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
