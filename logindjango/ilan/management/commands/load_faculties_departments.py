from django.core.management.base import BaseCommand
from ilan.models import Fakulte, Bolum

FACULTY_DEPARTMENTS = {
    "Mühendislik Fakültesi": [
        "Elektrik Mühendisliği",
        "Elektronik ve Haberleşme Mühendisliği",
        "Bilgisayar Mühendisliği",
        "Mekatronik Mühendisliği",
        "Endüstri Mühendisliği",
        "İnşaat Mühendisliği",
        "Makine Mühendisliği",
        "Metalurji ve Malzeme Mühendisliği",
        "Kimya Mühendisliği",
        "Harita Mühendisliği",
        "Çevre Mühendisliği",
        "Jeoloji Mühendisliği",
        "Jeofizik Mühendisliği",
        "Yazılım Mühendisliği"
    ],
    "Diş Hekimliği Fakültesi": [
        "Ağız, Diş ve Çene Cerrahisi",
        "Endodonti",
        "Diş Hekimliği"
    ],
    "Eğitim Fakültesi": [
        "Bilgisayar ve Öğretim Teknolojileri Eğitimi",
        "Eğitim Bilimleri",
        "Matematik ve Fen Bilimleri Eğitimi Bölümü",
        "İlköğretim (Temel Eğitim)",
        "Sosyal Bilgiler Eğitimi",
        "Türkçe Eğitimi",
        "Yabancı Diller Eğitimi"
    ],
    "Tıp Fakültesi": [
        "Temel Tıp Bilimleri",
        "Dahili Tıp Bilimleri",
        "Cerrahi Tıp Bilimleri"
    ],
    "Mimarlık ve Tasarım Fakültesi": [
        "Mimarlık",
        "İç Mimarlık",
        "Şehir ve Bölge Planlama",
        "Endüstriyel Tasarım"
    ],
    "Hukuk Fakültesi": [
        "Hukuk"
    ],
    "İktisadi ve İdari Bilimler Fakültesi": [
        "İşletme Bölümü",
        "İktisat Bölümü",
        "Finans, Bankacılık ve Sigortacılık",
        "Muhasebe ve Vergi",
        "Dış Ticaret",
        "Uluslararası Ticaret ve Lojistik",
        "Yönetim ve Organizasyon",
        "Çalışma Ekonomisi ve Endüstri İlişkileri",
        "Siyaset Bilimi ve Kamu Yönetimi",
        "Uluslararası İlişkiler"
    ],
    "Güzel Sanatlar Fakültesi": [
        "Resim",
        "Heykel",
        "Grafik Tasarımı Bölümü",
        "Fotoğraf Bölümü",
        "Müzik / Müzikoloji",
        "El Sanatları",
        "Geleneksel Türk Sanatları",
        "Seramik",
        "Türk Müziği"
    ],
    "İletişim Fakültesi": [
        "Gazetecilik",
        "Halkla İlişkiler ve Tanıtım",
        "Radyo, Sinema ve Televizyon",
        "Görsel İletişim Tasarımı",
        "Reklamcılık"
    ],
    "Teknoloji Fakültesi": [
        "Bilişim Sistemleri Mühendisliği",
        "Biyomedikal Mühendisliği",
        "Enerji Sistemleri Mühendisliği",
        "Otomotiv Mühendisliği"
    ],
    "Fen-Edebiyat Fakültesi": [
        "Türk Dili ve Edebiyatı",
        "Batı Dilleri ve Edebiyatları",
        "Felsefe",
        "Biyoloji",
        "Arkeoloji",
        "Tarih",
        "Matematik",
        "Fizik",
        "Kimya"
    ],
    "İlahiyat Fakültesi": [
        "Temel İslam Bilimleri",
        "Felsefe ve Din Bilimleri",
        "İslam Tarihi ve Sanatları"
    ],
    "Havacılık ve Uzay Bilimleri Fakültesi": [
        "Havacılık Elektrik ve Elektroniği",
        "Havacılık ve Uzay Mühendisliği Bölümü",
        "Havacılık Yönetimi",
        "Uçak Gövde ve Motor Bakımı"
    ],
    "Denizcilik Fakültesi": [
        "Denizcilik İşletmeleri Yönetimi",
        "Gemi Makineleri İşletme Mühendisliği",
        "Deniz Ulaştırma İşletme Mühendisliği"
    ],
    "Spor Bilimleri Fakültesi": [
        "Antrenörluk Eğitimi",
        "Beden Eğitimi ve Spor Bölümü",
        "Spor Yöneticiliği Bölümü",
        "Rekreasyon Bölümü"
    ],
    "Turizm Fakültesi": [
        "Turizm İşletmeciliği",
        "Turizm Rehberliği Bölümü",
        "Otel, Lokanta ve İkram Hizmetleri",
        "Seyahat-Turizm ve Eğlence Hizmetleri"
    ],
    "Ziraat Fakültesi": [
        "Bahçe Bitkileri Bölümü",
        "Bitki Koruma Bölümü",
        "Bitkisel ve Hayvansal Üretim",
        "Tarım Ekonomisi Bölümü",
        "Tekstil, Giyim, Ayakkabı ve Deri"
    ]
}

class Command(BaseCommand):
    help = 'Load all faculties and their departments'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Bolum.objects.all().delete()
        Fakulte.objects.all().delete()

        # Create faculties and departments
        for faculty_name, departments in FACULTY_DEPARTMENTS.items():
            faculty = Fakulte.objects.create(ad=faculty_name)
            self.stdout.write(self.style.SUCCESS(f'Created faculty: {faculty.ad}'))
            
            for dept_name in departments:
                department = Bolum.objects.create(
                    fakulte=faculty,
                    ad=dept_name
                )
                self.stdout.write(self.style.SUCCESS(f'Created department: {department.ad} in {faculty.ad}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all faculties and departments'))
