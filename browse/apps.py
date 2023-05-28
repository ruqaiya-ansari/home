from django.apps import AppConfig

class BrowseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'browse'

    def ready(self):
        # import signal handlers
       import browse.signals
