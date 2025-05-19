from django.db import models

from users.models import Profile


class Quote(models.Model):
    quote = models.CharField(max_length=300, unique=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=5)
    posted_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=300, default="Unknown")

    def __str__(self):
        return f"{self.quote} - {self.author} - By {self.user_profile}"

    def __unicode__(self):
        return self.quote
