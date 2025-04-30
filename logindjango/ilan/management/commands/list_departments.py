from django.core.management.base import BaseCommand
from ilan.models import Bolum, Fakulte

class Command(BaseCommand):
    help = 'List all departments and their associated faculties'

    def handle(self, *args, **kwargs):
        departments = Bolum.objects.all().select_related('fakulte')
        for department in departments:
            faculty_name = department.fakulte.ad if department.fakulte else 'None'
            self.stdout.write(self.style.SUCCESS(f'Department: {department.ad}, Faculty: {faculty_name}'))
