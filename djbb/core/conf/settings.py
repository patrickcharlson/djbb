from django.conf import settings as django_settings

from djbb.core.conf import defaults


class Settings:
    def __getattr__(self, item):
        try:
            return getattr(django_settings, item)
        except AttributeError:
            return getattr(defaults, item)


settings = Settings()
