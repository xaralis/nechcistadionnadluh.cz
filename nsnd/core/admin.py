from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site

from markdownx.admin import MarkdownxModelAdmin

from . import models


admin.site.unregister(Site)


class SiteProfileInline(admin.StackedInline):
    model = models.SiteProfile
    min_num = 1
    max_num = 1


@admin.register(models.Site)
class NSNDSiteAdmin(SiteAdmin):
    inlines = (SiteProfileInline,)

    def save_model(self, *args, **kwargs):
        super().save_model(*args, **kwargs)
        Site.objects.clear_cache()


@admin.register(models.FAQ)
class FAQ(MarkdownxModelAdmin):
    list_display = ("question", "priority")
    prepopulated_fields = {"slug": ("question",)}
