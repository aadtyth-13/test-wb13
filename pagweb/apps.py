from django.apps import AppConfig

class PagwebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pagweb"

    def ready(self):
        import pagweb.signals  # noqa