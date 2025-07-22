from allauth.account.signals import email_confirmed
from django.dispatch import receiver

@receiver(email_confirmed)
def set_email_verified(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True
    user.is_active = True
    user.save() 