from django.core.management.base import BaseCommand

from apps.core.keepalive import ping_banco


class Command(BaseCommand):
    help = "Executa uma consulta simples no banco para evitar que o Supabase entre em modo de pausa por inatividade."

    def handle(self, *args, **options):
        ping_banco()
        self.stdout.write(self.style.SUCCESS("Ping no banco de dados executado com sucesso."))
