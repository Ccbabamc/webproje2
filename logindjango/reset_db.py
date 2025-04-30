import os
import sys
import django
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Django projesinin yolunu ekle
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logindjango.settings')
django.setup()

from django.conf import settings

def reset_database():
    """
    PostgreSQL veritabanını sıfırlama işlemi
    """
    try:
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        user = db_settings['USER']
        password = db_settings['PASSWORD']
        host = db_settings['HOST']
        port = db_settings['PORT']
        
        # PostgreSQL'e template1 veritabanı üzerinden bağlan
        connection = psycopg2.connect(
            dbname='template1',
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        
        # Aktif bağlantıları kapat
        cursor.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{db_name}' AND pid <> pg_backend_pid();")
        
        # Veritabanını sil ve yeniden oluştur
        print(f"Veritabanı siliniyor: {db_name}")
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        print(f"Veritabanı oluşturuluyor: {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name} WITH OWNER = {user};")
        
        cursor.close()
        connection.close()
        
        print("Veritabanı başarıyla sıfırlandı!")
        
        # Migrationları uygula
        print("Migrationlar uygulanıyor...")
        os.system("python manage.py migrate")
        
        # Admin kullanıcısı oluştur
        print("Admin kullanıcısı oluşturuluyor...")
        os.system("python create_admin.py")
        
        print("İşlem tamamlandı!")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    confirm = input("Veritabanını sıfırlamak istediğinize emin misiniz? (e/h): ")
    if confirm.lower() == 'e':
        reset_database()
    else:
        print("İşlem iptal edildi.") 