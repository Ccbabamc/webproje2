# logindjango/ilan/management/commands/update_faculties.py
import os
import django

# Set up Django environment
# Ensure the DJANGO_SETTINGS_MODULE is correctly set for your project structure
# If manage.py is in the root 'logindjango' folder, this should be correct.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logindjango.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    # Consider raising the exception or exiting if setup fails
    import sys
    sys.exit(1)


from django.core.management.base import BaseCommand
from django.db import transaction
# Adjust the import based on your actual app structure if 'ilan' is not directly under the root
try:
    # Assuming 'ilan' app is directly under the project root alongside 'manage.py'
    from ilan.models import Fakulte
except ImportError as e:
     print(f"Could not import Fakulte from ilan.models: {e}. Check your project structure and PYTHONPATH.")
     # If the script is run via manage.py, Django usually handles the path.
     # This might indicate an issue if run directly without manage.py context.
     import sys
     sys.exit(1) # Exit if model cannot be imported


class Command(BaseCommand):
    help = 'Updates the Fakulte table with the provided list, adding new ones.'

    # List of faculty names provided by the user
    new_faculty_names = [
        "Adalet Meslek Yüksekokulu",
        "Ali Rıza Veziroğlu Meslek Yüksekokulu",
        "Değirmendere Ali Özbay Meslek Yüksekokulu",
        "Denizcilik Fakültesi",
        "Devlet Konservatuvarı",
        "Diş Hekimliği Fakültesi",
        "Eğitim Fakültesi",
        "Fen - Edebiyat Fakültesi",
        "Fen Bilimleri Enstitüsü",
        "Ford Otosan İhsaniye Otomotiv Meslek Yüksekokulu",
        "Gastroenteroloji ve Hepatoloji Enstitüsü",
        "Gazanfer Bilge Meslek Yüksekokulu",
        "Gölcük Meslek Yüksekokulu",
        "Güzel Sanatlar Fakültesi",
        "Havacılık ve Uzay Bilimleri Fakültesi",
        "Hereke Asım Kocabıyık Meslek Yüksekokulu",
        "Hereke Ö.İ. Uzunyol Meslek Yüksekokulu",
        "Hukuk Fakültesi",
        "İlahiyat Fakültesi",
        "İletişim Fakültesi",
        "İşletme Fakültesi",
        "İzmit Meslek Yüksekokulu",
        "Kandıra Meslek Yüksekokulu",
        "Karamürsel Denizcilik Meslek Yüksekokulu",
        "Kartepe Atçılık Meslek Yüksekokulu",
        "Kartepe Turizm Meslek Yüksekokulu",
        "Kocaeli Meslek Yüksekokulu",
        "Kocaeli Sağlık Hizmetleri Meslek Yüksekokulu",
        "Mimarlık ve Tasarım Fakültesi",
        "Mühendislik Fakültesi",
        "REKTÖRLÜK", # Assuming this is treated as a faculty/unit
        "Sağlık Bilimleri Enstitüsü",
        "Sağlık Bilimleri Fakültesi",
        "Siyasal Bilgiler Fakültesi",
        "Sosyal Bilimler Enstitüsü",
        "Spor Bilimleri Fakültesi",
        "Teknoloji Fakültesi",
        "Tıp Fakültesi",
        "Turizm Fakültesi",
        "Ulaştırma Yüksekokulu",
        "Uzunçiftlik Nuh Çimento Meslek Yüksekokulu",
        "Yabancı Diller Yüksekokulu",
        "Ziraat Fakültesi"
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Updating faculties...'))

        added_count = 0
        existing_count = 0

        # Add or update faculties from the new list
        for name in self.new_faculty_names:
            faculty, created = Fakulte.objects.update_or_create(
                ad=name,
                defaults={'ad': name} # Ensure the name is set correctly
            )
            if created:
                added_count += 1
                self.stdout.write(f'Added: {name}')
            else:
                existing_count += 1
                # self.stdout.write(f'Exists: {name}') # Optional: log existing ones

        total_processed = len(self.new_faculty_names)
        self.stdout.write(self.style.SUCCESS(f'Faculty update complete. Processed: {total_processed}. Added: {added_count}, Existing: {existing_count}.'))

        # --- Optional: Delete faculties not in the new list ---
        # Be cautious using delete operations, especially if departments depend on them.
        # Consider adding a command-line flag to enable deletion.
        # delete_obsolete = options.get('delete_obsolete', False) # Example flag
        # if delete_obsolete:
        #     current_faculties = Fakulte.objects.values_list('ad', flat=True)
        #     faculties_to_delete = set(current_faculties) - set(self.new_faculty_names)
        #     if faculties_to_delete:
        #         self.stdout.write(self.style.WARNING(f'Deleting {len(faculties_to_delete)} faculties not in the provided list...'))
        #         # Check for dependent departments before deleting if necessary
        #         deleted_count, deleted_details = Fakulte.objects.filter(ad__in=faculties_to_delete).delete()
        #         self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} faculties.'))
        #         # print(deleted_details) # Shows counts per model type deleted
        #     else:
        #         self.stdout.write('No obsolete faculties to delete.')
