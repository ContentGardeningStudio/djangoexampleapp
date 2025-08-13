# from server.settings.components import config
import os

from dotenv import load_dotenv

load_dotenv()


EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = BASE_DIR / "app-messages"

# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"  # or amazon_ses.EmailBackend, or...

ANYMAIL = {
    "BREVO_API_KEY": os.environ.get("BREVO_API_KEY"),
    #     "MAILGUN_API_KEY": config('MAILGUN_API_KEY'),
    #     "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    #     "MAILGUN_SENDER_DOMAIN": 'mydomain.com',  # your Mailgun domain, if needed
}
# DEFAULT_FROM_EMAIL = "contact@mydomain.com"  # if you don't already have this in settings
# # SERVER_EMAIL = "your-server@example.com"  # ditto (default from-email for Django errors)
