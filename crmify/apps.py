from django.apps import AppConfig


class CrmifyConfig(AppConfig):
    name = 'crmify'

    def ready(self):
        import crmify.signals