from django.apps import AppConfig


class PrimaryTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'primary_test'

    def ready(self):
        import primary_test.signals