from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default groups and assign permissions"

    def handle(self, *args, **kwargs):
        # User = get_user_model()
        # Profile = apps.get_model('accounts.Profile')

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

        self.stdout.write(
            self.style.SUCCESS("Groups and permissions set up successfully")
        )
