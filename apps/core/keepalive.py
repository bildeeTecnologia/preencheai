"""Rotina de keepalive: evita que o projeto Supabase entre em modo de pausa por inatividade."""
import logging
import threading
import time

from django.conf import settings
from django.db import connection

logger = logging.getLogger(__name__)


def ping_banco():
    """Executa uma consulta simples (SELECT 1) para gerar atividade no banco."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()


def _loop(intervalo_segundos):
    while True:
        try:
            ping_banco()
            logger.info("Keepalive Supabase: ping executado com sucesso.")
        except Exception:
            logger.exception("Keepalive Supabase: falha ao executar ping.")
        time.sleep(intervalo_segundos)


def iniciar_keepalive():
    """Inicia uma thread em background que faz ping periodico no banco."""
    if not getattr(settings, "SUPABASE_KEEPALIVE_ENABLED", False):
        return

    intervalo_horas = getattr(settings, "SUPABASE_KEEPALIVE_INTERVAL_HOURS", 12)
    thread = threading.Thread(
        target=_loop,
        args=(intervalo_horas * 3600,),
        daemon=True,
        name="supabase-keepalive",
    )
    thread.start()
