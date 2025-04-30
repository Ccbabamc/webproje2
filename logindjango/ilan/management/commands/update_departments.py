# logindjango/ilan/management/commands/update_departments.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logindjango.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    import sys
    sys.exit(1)

from django.core.management.base import BaseCommand
from django.db import transaction
try:
    from ilan.models import Bolum
except ImportError as e:
     print(f"Could not import Bolum from ilan.models: {e}. Check your project structure and PYTHONPATH.")
     import sys
     sys.exit(1)

class Command(BaseCommand):
    help = 'Updates the Bolum table with the provided list, adding new ones.'

    # List of department names provided by the user
    # Note: Duplicates are kept as provided in the original list.
    # Consider cleaning this list if duplicates are not desired.
    new_department_names = [
        "Antrenörluk Eğitimi",
        "Arkeoloji",
        "Atatürk Devrimleri ve İlkeleri Arş.Uyg.Mrk.",
        "Atatürk İlkeleri ve İnkılap Tarihi",
        "Bahçe Bitkileri Bölümü",
        "Batı Dilleri ve Edebiyatları",
        "Beden Eğitimi ve Spor Bölümü",
        "Bilgisayar Mühendisliği",
        "Bilgisayar Teknolojileri",
        "Bilgisayar ve Öğretim Teknolojileri Eğitimi",
        "Bilişim Sistemleri Mühendisliği",
        "Bitki Koruma Bölümü",
        "Bitkisel ve Hayvansal Üretim",
        "Bitkisel ve Hayvansal Üretim",
        "Biyoloji",
        "Biyomedikal Mühendisliği",
        "Büro Hizmetleri ve Sekreterlik",
        "Büro Hizmetleri ve Sekreterlik",
        "Cerrahi Tıp Bilimleri",
        "Çalışma Ekonomisi ve Endüstri İlişkileri",
        "Çevre Koruma Teknolojileri",
        "Çevre Mühendisliği",
        "Çevre Temizlik Hizmetleri",
        "ÇEVSAM",
        "Dahili Tıp Bilimleri",
        "Deniz Ulaştırma İşletme Mühendisliği",
        "Denizcilik İşletmeleri Yönetimi",
        "Dış Ticaret",
        "Dış Ticaret",
        "Ebelik Bölümü",
        "Eğitim Bilimleri",
        "El Sanatları",
        "Elektrik Mühendisliği",
        "Elektrik ve Enerji",
        "Elektrik ve Enerji",
        "Elektrik ve Enerji",
        "Elektronik ve Haberleşme Mühendisliği",
        "Elektronik ve Otomasyon",
        "Elektronik ve Otomasyon",
        "Elektronik ve Otomasyon",
        "Endüstri Mühendisliği",
        "Endüstriyel Tasarım",
        "Enerji Sistemleri Mühendisliği",
        "Enformatik Bölümü",
        "Felsefe",
        "Felsefe ve Din Bilimleri",
        "Fen Bilimleri Enstitüsü",
        "Finans-Bankacılık ve Sigortacılık",
        "Finans-Bankacılık ve Sigortacılık",
        "Fizik",
        "Fotoğraf Bölümü",
        "Gastroenteroloji ve Hepatoloji Bölümü",
        "Gastronomi ve Mutfak Sanatları",
        "Gazetecilik",
        "Geleneksel Türk Sanatları",
        "Gemi Makineleri İşletme Mühendisliği",
        "Gıda İşleme",
        "Görsel İletişim Tasarımı",
        "Görsel, İşitsel Teknikler ve Medya Yapımcılığı",
        "Grafik Tasarımı Bölümü",
        "Halkla İlişkiler ve Tanıtım",
        "Harita Mühendisliği",
        "Havacılık Elektrik ve Elektroniği",
        "Havacılık ve Uzay Mühendisliği Bölümü",
        "Havacılık Yönetimi",
        "Hemşirelik Bölümü",
        "Heykel",
        "Hukuk",
        "İç Mimarlık",
        "İktisat Bölümü",
        "İnşaat",
        "İnşaat",
        "İnşaat Mühendisliği",
        "İslam Tarihi ve Sanatları",
        "İşletme Bölümü",
        "Jeofizik Mühendisliği",
        "Jeoloji Mühendisliği",
        "Kamu Hukuku",
        "Kimya",
        "Kimya Mühendisliği",
        "Kimya ve Kimyasal İşleme Teknolojileri",
        "Kimya ve Kimyasal İşleme Teknolojileri",
        "Klinik Bilimler",
        "Makine Mühendisliği",
        "Makine ve Metal Teknolojileri",
        "Makine ve Metal Teknolojileri",
        "Makine ve Metal Teknolojileri",
        "Makine ve Metal Teknolojileri",
        "Makine ve Metal Teknolojileri",
        "Matematik",
        "Matematik ve Fen Bilimleri Eğitimi Bölümü",
        "Mekatronik Mühendisliği",
        "Metalurji ve Malzeme Mühendisliği",
        "Mimarlık",
        "Mimarlık Bölümü",
        "Motorlu Araçlar ve Ulaşım Teknolojileri",
        "Motorlu Araçlar ve Ulaştırma Teknolojileri",
        "Motorlu Araçlar ve Ulaştırma Teknolojileri",
        "Muhasebe ve Vergi",
        "Muhasebe ve Vergi",
        "Muhasebe ve Vergi",
        "Mülkiyet Koruma ve Güvenlik",
        "Mülkiyet Koruma ve Güvenlik",
        "Müzik",
        "Müzik",
        "Müzikoloji",
        "Otel, Lokanta ve İkram Hizmetleri",
        "Otomotiv Mühendisliği",
        "Özel Eğitim",
        "Özel Hukuk",
        "Pazarlama ve Reklamcılık",
        "Pazarlama ve Reklamcılık",
        "Pazarlama ve Reklamcılık",
        "Psikoloji",
        "Radyo, Sinema ve Televizyon",
        "Reklamcılık",
        "Rekreasyon Bölümü",
        "REKTÖRLÜK",
        "Resim",
        "Sağlık Bakım Hizmetleri Bölümü",
        "Sahne Sanatları",
        "Seramik",
        "Seyahat-Turizm ve Eğlence Hizmetleri",
        "Siyaset Bilimi ve Kamu Yönetimi Bölümü",
        "Sosyal Bilimler Enstitüsü",
        "Sosyal Hizmet Bölümü",
        "Spor Yöneticiliği Bölümü",
        "Şehir ve Bölge Planlama",
        "Tarım Ekonomisi Bölümü",
        "Tarih",
        "Taşınabilir Kül. Varl. Koruma ve Onarım",
        "Tekstil, Giyim, Ayakkabı ve Deri",
        "Temel Eğitim",
        "Temel Eğitim",
        "Temel İslam Bilimleri",
        "Temel Tıp Bilimleri",
        "Terapi ve Rehabilitasyon Bolumu",
        "Tıbbi Hizmetler ve Teknikler",
        "Toptan ve Perakende Satış",
        "Turizm İşletmeciliği",
        "Turizm Rehberliği Bölümü",
        "Türk Dili Bölümü",
        "Türk Dili ve Edebiyatı",
        "Türk Müziği",
        "Türkçe ve Sosyal Bilimler Eğitimi",
        "Uçak Gövde ve Motor Bakımı",
        "Ulaştırma Hizmetleri",
        "Uluslararası İlişkiler Bölümü",
        "Uluslararası Ticaret ve Lojistik",
        "Yabancı Diller Bölümü",
        "Yabancı Diller Eğitimi",
        "Yazılım Mühendisliği",
        "Yönetim ve Organizasyon",
        "Yönetim ve Organizasyon",
        "Yönetim ve Organizasyon",
        "Yönetim ve Organizasyon",
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Updating departments (Bölümler)...'))

        added_count = 0
        existing_count = 0
        unique_department_names = set(self.new_department_names) # Use set for efficiency and uniqueness

        # Add or update departments from the new list
        for name in unique_department_names:
            # Since fakulte is now optional (null=True), we don't need to specify it here.
            # We only match/create based on the department name ('ad').
            department, created = Bolum.objects.update_or_create(
                ad=name,
                defaults={'ad': name} # Ensure the name is set correctly
            )
            if created:
                added_count += 1
                self.stdout.write(f'Added: {name}')
            else:
                existing_count += 1
                # self.stdout.write(f'Exists: {name}') # Optional: log existing ones

        total_processed = len(unique_department_names)
        self.stdout.write(self.style.SUCCESS(f'Department update complete. Processed: {total_processed}. Added: {added_count}, Existing: {existing_count}.'))

        # Optional: Delete departments not in the new list (use with caution)
        # delete_obsolete = options.get('delete_obsolete', False)
        # if delete_obsolete:
        #     current_departments = Bolum.objects.values_list('ad', flat=True)
        #     departments_to_delete = set(current_departments) - unique_department_names
        #     if departments_to_delete:
        #         self.stdout.write(self.style.WARNING(f'Deleting {len(departments_to_delete)} departments not in the provided list...'))
        #         deleted_count, _ = Bolum.objects.filter(ad__in=departments_to_delete).delete()
        #         self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} departments.'))
        #     else:
        #         self.stdout.write('No obsolete departments to delete.')
