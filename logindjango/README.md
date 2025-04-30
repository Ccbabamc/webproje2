# Akademik Başvuru Sistemi

Bu proje, akademik başvuruların yönetimi için geliştirilmiş bir Django REST API uygulamasıdır.

## Özellikler

- Kullanıcı yönetimi (Admin, Yönetici, Jüri Üyesi, Aday)
- İlan yönetimi (Fakülte, Bölüm, Kriter, İlan)
- Başvuru yönetimi (Başvuru, Belge, Tablo 5, Puan)
- JWT tabanlı kimlik doğrulama
- Rol tabanlı yetkilendirme
- API dokümantasyonu (Swagger/ReDoc)
- Dosya yükleme desteği
- Filtreleme ve arama özellikleri

## Gereksinimler

- Python 3.8+
- Redis
- PostgreSQL (önerilen)

## Kurulum

1. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Veritabanı ayarlarını yapın:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Süper kullanıcı oluşturun:
```bash
python manage.py createsuperuser
```

5. Geliştirme sunucusunu başlatın:
```bash
python manage.py runserver
```

## API Dokümantasyonu

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Kullanıcı Rolleri

### Admin
- Tüm sistem yönetimi
- Kullanıcı yönetimi
- İlan yönetimi
- Başvuru değerlendirme

### Yönetici
- İlan yönetimi
- Başvuru değerlendirme
- Raporlama

### Jüri Üyesi
- Başvuru değerlendirme
- Puanlama

### Aday
- İlan görüntüleme
- Başvuru yapma
- Belge yükleme
- Tablo 5 oluşturma

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 