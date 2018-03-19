from django.apps import AppConfig


class RestConfig(AppConfig):
    name = 'unfold.rest'
    verbose_name = "Rest"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
