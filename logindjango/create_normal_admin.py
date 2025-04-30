import os
import sys
import django

# Django projesinin path'ini ekle
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logindjango'))
sys.path.append(project_path)

# Django ortamını ayarla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logindjango.settings')
django.setup()

from users.models import User

try:
    # Normal admin kullanıcısı oluştur
    admin = User.objects.create_user(
        username='normaladmin',  # Normal admin kullanıcı adı
        email='normaladmin@example.com',  # Email adresi
        password='Elif1036xd.',
        tc_kimlik_no='38545676060'  # Farklı bir TC kimlik no
    )

    # Kullanıcıya admin yetkileri ver
    admin.is_staff = True
    admin.is_superuser = False  # normal admin için superuser değil
    admin.role = 'admin'  # SUPERADMIN değil, normal admin
    admin.save()

    print("Normal admin kullanıcısı başarıyla oluşturuldu!")
except Exception as e:
    print(f"Hata oluştu: {e}")