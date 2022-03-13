from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ExampleAppConfig(AppConfig):
    name = "stockze.example_app"
    verbose_name = _("ExampleApp")