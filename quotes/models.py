from django.db import models

from accounts.models import Profile


class QuoteAuthor(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.CharField(max_length=300, unique=True)
    poster = models.ForeignKey(
        Profile, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    posted_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(QuoteAuthor, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.quote} - {self.author} - By {self.poster}"
