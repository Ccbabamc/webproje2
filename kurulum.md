# KOÜ Akademik Personel Başvuru Sistemi - Kurulum Rehberi

Bu belge, Akademik Personel Başvuru Sistemi'nin geliştirme ve canlı ortamlarının kurulumu için adım adım talimatlar içermektedir.

## İçindekiler

1. Ön Gereksinimler
2. Geliştirme Ortamı Kurulumu
3. Backend Kurulumu
4. Frontend Kurulumu
5. Veritabanı Kurulumu
6. Çalıştırma
7. Docker ile Kurulum
8. Canlı Ortam Kurulumu
9. Sorun Giderme

## 1. Ön Gereksinimler

Aşağıdaki yazılımların kurulu olması gerekmektedir:

- Python 3.9 veya üzeri
- Node.js 16 veya üzeri
- npm 7 veya üzeri
- PostgreSQL 14 veya üzeri
- Git
- Docker ve Docker Compose (opsiyonel)

## 2. Geliştirme Ortamı Kurulumu

### 2.1. Projeyi Klonlama

```bash
git clone https://github.com/kocaeli-universitesi/akademik-personel-basvuru.git
cd akademik-personel-basvuru
```

### 2.2. Sanal Ortam Oluşturma (Python)

Windows için:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Linux/macOS için:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Backend Kurulumu

### 3.1. Bağımlılıkları Yükleme

```bash
cd src/backend
pip install -r requirements.txt
```

### 3.2. Ortam Değişkenlerini Ayarlama

`.env` dosyasını oluşturun:

```
DEBUG=True
SECRET_KEY=your_development_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/akademik_basvuru
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080
```

### 3.3. Veritabanı Migrasyonları

```bash
python manage.py migrate
```

### 3.4. Örnek Veri Oluşturma (Opsiyonel)

```bash
python manage.py loaddata initial_data
```

### 3.5. Admin Kullanıcısı Oluşturma

```bash
python manage.py createsuperuser
```

## 4. Frontend Kurulumu

### 4.1. Bağımlılıkları Yükleme

```bash
cd src/frontend
npm install
```

### 4.2. Ortam Değişkenlerini Ayarlama

`.env` dosyasını oluşturun:

```
VUE_APP_API_URL=http://localhost:8000/api
VUE_APP_TITLE=KOÜ Akademik Personel Başvuru Sistemi
```

## 5. Veritabanı Kurulumu

### 5.1. PostgreSQL Kurulumu

Windows için:
- [PostgreSQL indirme sayfası](https://www.postgresql.org/download/windows/)
- Kurulum sihirbazını takip edin

Linux için:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### 5.2. Veritabanı Oluşturma

```bash
sudo -u postgres psql
```

PostgreSQL konsolunda:
```sql
CREATE DATABASE akademik_basvuru;
CREATE USER akademik_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE akademik_basvuru TO akademik_user;
\q
```

## 6. Çalıştırma

### 6.1. Backend Sunucusunu Başlatma

```bash
cd src/backend
python manage.py runserver
```

Backend API http://localhost:8000/ adresinde çalışacaktır.

### 6.2. Frontend Geliştirme Sunucusunu Başlatma

```bash
cd src/frontend
npm run serve
```

Frontend uygulama http://localhost:8080/ adresinde çalışacaktır.

## 7. Docker ile Kurulum

### 7.1. Docker Compose ile Çalıştırma

Projenin kök dizininde:

```bash
docker-compose up -d
```

Bu komut aşağıdaki servisleri başlatacaktır:
- Backend: http://localhost:8000/
- Frontend: http://localhost:8080/
- PostgreSQL: localhost:5432
- Nginx (opsiyonel): http://localhost/

### 7.2. Docker Loglarını İzleme

```bash
docker-compose logs -f
```

## 8. Canlı Ortam Kurulumu

Canlı ortam kurulumu için aşağıdaki adımları takip edin:

### 8.1. Güvenlik Ayarları

Canlı ortam için `.env` dosyasında aşağıdaki değişiklikleri yapın:
```
DEBUG=False
SECRET_KEY=your_secure_production_key
ALLOWED_HOSTS=your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com
```

### 8.2. Statik Dosyaları Toplama

```bash
python manage.py collectstatic
```

### 8.3. Nginx Yapılandırması

Örnek Nginx konfigürasyonu:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/backend/staticfiles;
    }
    
    location /media {
        alias /path/to/backend/media;
    }
}
```

### 8.4. SSL Sertifikası (Let's Encrypt)

```bash
sudo certbot --nginx -d your-domain.com
```

## 9. Sorun Giderme

### 9.1. Veritabanı Bağlantı Hataları

- PostgreSQL servisinin çalıştığından emin olun
- Veritabanı bilgilerinin doğruluğunu kontrol edin
- Kullanıcının yeterli yetkiye sahip olduğunu doğrulayın

### 9.2. Frontend-Backend Bağlantı Sorunları

- CORS ayarlarını kontrol edin
- API URL'sinin doğru olduğunu doğrulayın
- Ağ bağlantısını test edin

### 9.3. Docker Sorunları

- Docker servisinin çalıştığından emin olun
- Port çakışmalarını kontrol edin
- Docker loglarını inceleyerek hata mesajlarını tespit edin 