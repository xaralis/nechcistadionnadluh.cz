from django.db import models
from django.contrib.sites.models import Site


class SiteProfile(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="profile")
    votes_collected = models.PositiveIntegerField(verbose_name="Počet sesbíraných hlasů", null=False, blank=False, default=0)
    votes_targeted = models.PositiveIntegerField(verbose_name="Cílový počet sesbíraných hlasů", null=False, blank=False, default=8000)
