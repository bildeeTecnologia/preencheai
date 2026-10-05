import os
import shutil
import sys
import warnings

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core"

    def ready(self):
        from django.conf import settings

        if not shutil.which(settings.LIBREOFFICE_PATH):
            warnings.warn(
                f"LIBREOFFICE_PATH='{settings.LIBREOFFICE_PATH}' nao encontrado no PATH. "
                "Geracao de PDF estara desabilitada.",
                RuntimeWarning,
                stacklevel=2,
            )

        is_gunicorn = "gunicorn" in sys.argv[0]
        is_runserver_child = "runserver" in sys.argv and os.environ.get("RUN_MAIN") == "true"
        if is_gunicorn or is_runserver_child:
            from .keepalive import iniciar_keepalive

            iniciar_keepalive()
