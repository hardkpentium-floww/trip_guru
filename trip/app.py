from django.apps import AppConfig

class TripAppConfig(AppConfig):
    name = "trip"

    def ready(self):
        from trip import signals # pylint: disable=unused-variable
