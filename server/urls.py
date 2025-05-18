from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path

from quotes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.list_quotes, name="list_quotes"),
    path("contact", views.contact, name="contact"),
] + debug_toolbar_urls()
