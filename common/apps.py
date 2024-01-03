from importlib import import_module
from django.apps import AppConfig
from . import signals  # Import signals directly

class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    def ready(self):
        pass  # Since we've already imported signals, we can leave this method empty or remove it
        # import_module('.signals', package='common')
