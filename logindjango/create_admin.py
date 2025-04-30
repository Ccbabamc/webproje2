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
    # Admin kullanıcısı oluştur
    admin = User.objects.create_user(
        username='localadmin',  # admin yerine localadmin kullanıcı adı
        email='localadmin@example.com',  # yeni email adresi
        password='12345678',
        tc_kimlik_no='12345678901'  # yeni TC kimlik no
    )

    # Kullanıcıya admin yetkileri ver
    admin.is_staff = True
    admin.is_superuser = True
    admin.role = 'SUPERADMIN'
    admin.save()

    print("Local admin kullanıcısı başarıyla oluşturuldu!")
except Exception as e:
    print(f"Hata oluştu: {e}")