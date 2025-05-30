from django.db import models
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from taggit.managers import TaggableManager

from accounts.models import Profile


class QuoteAuthor(models.Model):
    name = models.CharField(max_length=300)
    country = CountryField(null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Quote(models.Model):
    quote = models.CharField(max_length=300, unique=True)
    poster = models.ForeignKey(
        Profile, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    posted_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(QuoteAuthor, on_delete=models.DO_NOTHING)
    tags = TaggableManager()

    def __str__(self):
        return f"{self.quote} - {self.author} - By {self.poster}"
