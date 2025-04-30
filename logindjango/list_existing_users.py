import os
import django

# Django ortamını ayarla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logindjango.settings') 
django.setup()

from users.models import User

print("Sistemdeki Mevcut Kullanıcılar:")
print("--------------------------------")

users = User.objects.all().order_by('id')

if not users:
    print("Sistemde kayıtlı kullanıcı bulunamadı.")
else:
    for user in users:
        print(f"ID: {user.id}")
        print(f"  Username (TC): {user.username}")
        print(f"  TC Kimlik No: {user.tc_kimlik_no}")
        print(f"  Email: {user.email}")
        print(f"  Ad Soyad: {user.first_name} {user.last_name}")
        print(f"  Rol: {user.get_role_display()}") # Display name of the role
        print(f"  Aktif Mi?: {user.is_active}")
        print(f"  Staff Mı?: {user.is_staff}")
        print(f"  Superuser Mı?: {user.is_superuser}")
        print("-" * 20)

print("--------------------------------")
print(f"Toplam {users.count()} kullanıcı listelendi.")
