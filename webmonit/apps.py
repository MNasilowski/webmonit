from django.apps import AppConfig



class WebmonitConfig(AppConfig):
    name = 'webmonit'

    def ready(self):
        from webmonit import signals
