from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


User = get_user_model()


@receiver(email_confirmed)
def set_email_verified(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True
    user.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from accounts.models import Profile
    
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
