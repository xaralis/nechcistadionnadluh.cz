from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from nsnd.core.models import SiteProfile


def global_info(request):
    return {
        "siteinfo": settings.SITEINFO,
    }


def votes(request):
    site = get_current_site(request)

    try:
        profile = SiteProfile.objects.get(site=site)
        return {
            "votes_collected": profile.votes_collected,
            "votes_targeted": profile.votes_targeted,
            "votes_percent": (profile.votes_collected / profile.votes_targeted) * 100
            if profile.votes_targeted > 0
            else 0,
        }
    except Exception as exc:
        return {
            "votes_collected": 0,
            "votes_targeted": 0,
            "votes_percent": 0,
        }
