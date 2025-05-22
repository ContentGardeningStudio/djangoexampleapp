from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path

from quotes import views as quotes_views
from users import views as users_views

urlpatterns = [
    path("", quotes_views.home, name="home"),
    path("admin/", admin.site.urls),
    path("register/", users_views.register_view, name="register"),
    path("login/", users_views.login_view, name="login"),
    path("profile/", users_views.profile_view, name="profile"),
    path("profile/edit/", users_views.edit_profile_view, name="edit_profile"),
    path("logout/", users_views.custom_logout_view, name="logout"),
] + debug_toolbar_urls()
