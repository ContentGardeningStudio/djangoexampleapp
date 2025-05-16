from django.db import models

from users.models import User


class Quote(models.Model):
    quote = models.CharField(max_length=300, unique=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=300, default="Unknown")

    def __str__(self):
        return f"{self.quote} - {self.author} - By {self.poster}"

    def __unicode__(self):
        return self.quote
