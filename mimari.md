# KOÜ Akademik Personel Başvuru Sistemi - Mimari Doküman

## 1. Genel Mimari

Sistem, üç katmanlı bir mimari üzerine kurulmuştur:

### 1.1. Sunum Katmanı (Frontend)
- **Teknoloji**: Vue.js (v3)
- **Durum Yönetimi**: Pinia
- **HTTP İstekleri**: Axios
- **UI Kütüphanesi**: Vuetify veya TailwindCSS

### 1.2. İş Mantığı Katmanı (Backend)
- **Teknoloji**: Django REST Framework
- **Kimlik Doğrulama**: JWT (JSON Web Token)
- **API Dökümantasyonu**: OpenAPI (Swagger)

### 1.3. Veri Erişim Katmanı
- **Veritabanı**: PostgreSQL
- **ORM**: Django ORM
- **Veri Yedekleme**: Otomatik günlük yedekleme

## 2. Sistem Bileşenleri

### 2.1. Kullanıcı Yönetimi ve Kimlik Doğrulama
- 4 Kullanıcı rolü (Aday, Admin, Yönetici, Jüri)
- e-Devlet entegrasyonu
- Rol bazlı yetkilendirme

### 2.2. İlan Yönetimi
- İlan oluşturma, düzenleme, filtreleme
- Başlangıç/bitiş tarihi kontrolü
- Fakülte/bölüm bazlı kategorilendirme

### 2.3. Başvuru İşleme
- Çok adımlı başvuru formu
- Belge yükleme ve doğrulama
- Başvuru durumu takibi

### 2.4. Kriter Yönetimi ve Puanlama
- Dinamik kriter tanımlama
- Otomatik puan hesaplama
- Tablo 5 oluşturma

### 2.5. Değerlendirme Süreci
- Jüri atama
- Rapor yükleme
- Nihai karar verme

### 2.6. Bildirim Sistemi
- E-posta bildirimleri
- Sistem içi bildirimler

### 2.7. Raporlama
- PDF rapor üretimi
- İstatistik görüntüleme

## 3. Veri Modeli

Ana veri modelleri şunlardır:

- Kullanıcı (User)
- İlan (Announcement)
- Başvuru (Application)
- Belge (Document)
- Kriter (Criteria)
- Değerlendirme (Evaluation)
- Bildirim (Notification)

## 4. Güvenlik Önlemleri

- HTTPS zorunluluğu
- JWT tabanlı kimlik doğrulama
- XSS ve CSRF koruması
- İşlem logları
- Veri şifreleme
- Rol bazlı erişim kontrolü

## 5. Performans Optimizasyonu

- Frontend için lazy loading
- API cevapları için önbellekleme
- Veritabanı sorgu optimizasyonu
- Dosya sıkıştırma

## 6. Ölçeklenebilirlik

- Docker konteynerleştirilmesi
- Yük dengeleyici (Load Balancer) desteği
- Otomatik yatay ölçeklenebilirlik (Horizontal Auto-Scaling)

## 7. İzleme ve Loglama

- Uygulama performans izleme
- Kullanıcı etkileşim analizi
- Hata loglama ve bildirimi 