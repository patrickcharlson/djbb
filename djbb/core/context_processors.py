from djbb.core.conf import settings as djbb_settings


def forum_settings(request):
    return {
        "settings": djbb_settings
    }
