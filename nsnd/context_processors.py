from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def global_info(request):
    return {
        "siteinfo": settings.SITEINFO,
    }


def votes(request):
    site = get_current_site(request)

    try:
        profile = site.profile
        return {
            "votes_collected": profile.votes_collected,
            "votes_targeted": profile.votes_targeted,
        }
    except Exception as exc:
        return {
            "votes_collected": 0,
            "votes_targeted": 0,
        }

