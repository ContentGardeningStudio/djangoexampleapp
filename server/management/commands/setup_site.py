from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


def initialize_groups():
    # Create or get groups
    admins, _ = Group.objects.get_or_create(name="Administrators")
    members, _ = Group.objects.get_or_create(name="Members")

    # Admin group: all permissions
    admin_perms = Permission.objects.filter(
        content_type__app_label__in=["auth", "accounts", "quotes"],
    )
    admins.permissions.set(admin_perms)

    # Member group: only view and change their own profile + adding quotes
    profile_perms = Permission.objects.filter(
        codename__in=[
            "view_profile",
            "change_profile",
        ]
    )
    quote_perms = Permission.objects.filter(
        codename__in=[
            "add_quote",
            "view_quote",
        ]
    )
    combined_perms = profile_perms | quote_perms  # union
    members.permissions.set(combined_perms)


def initialize_socialaccount_auth():
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


class Command(BaseCommand):
    help = "Initial application setup actions"

    def handle(self, *args, **kwargs):
        initialize_groups()
        self.stdout.write(
            self.style.SUCCESS("Groups and permissions set up successfully")
        )

        initialize_socialaccount_auth()
        self.stdout.write(self.style.SUCCESS("Social account auth set up successfully"))
