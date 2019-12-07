from django.db import models
from django.contrib.sites.models import Site

from markdownx.models import MarkdownxField


class SiteProfile(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="profile")
    votes_collected = models.PositiveIntegerField(verbose_name="Počet sesbíraných hlasů", null=False, blank=False, default=0)
    votes_targeted = models.PositiveIntegerField(verbose_name="Cílový počet sesbíraných hlasů", null=False, blank=False, default=8000)

    class Meta:
        verbose_name = "Profil stránky"
        verbose_name_plural = "Profily stránek"


class FAQ(models.Model):
    question = models.TextField(verbose_name="Otázka", null=False, blank=False)
    answer = MarkdownxField(verbose_name="Odpověď", null=False, blank=False)
    slug = models.SlugField(verbose_name="Slug", null=False, blank=False)
    priority = models.SmallIntegerField(verbose_name="Priorita", help_text="Čím vyšší, tím víc nahoře.", null=False, blank=False, default=0)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ("priority", "question")

    def __str__(self):
        return self.question
