import sys

from django.apps import AppConfig
from django.conf import settings


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        if "runserver" not in sys.argv and "gunicorn" not in sys.argv:
            return

        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site

        # Avoid premature model access: get from app registry
        # Not strictly needed for SocialApp, but safe practice
        if not SocialApp.objects.filter(provider="google").exists():
            site = Site.objects.get_current()
            app = SocialApp.objects.create(
                provider="google",
                name="Google",
                client_id=settings.SOCIALACCOUNT_APPS["google"]["client_id"],
                secret=settings.SOCIALACCOUNT_APPS["google"]["secret"],
            )
            app.sites.add(site)
