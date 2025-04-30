from django.core.management.base import BaseCommand
from ilan.models import Fakulte

class Command(BaseCommand):
    help = 'List all faculties'

    def handle(self, *args, **kwargs):
        faculties = Fakulte.objects.all()
        for faculty in faculties:
            self.stdout.write(self.style.SUCCESS(f'Faculty: {faculty.ad}'))
