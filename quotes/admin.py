from django.contrib import admin

from .models import Quote, QuoteAuthor

admin.site.register(Quote)


class QuoteAuthorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
    )
    prepopulated_fields = {"slug": ("name".lower().replace(" ", "-"),)}


admin.site.register(QuoteAuthor, QuoteAuthorAdmin)
