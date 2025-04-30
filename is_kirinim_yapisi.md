# KOÜ Akademik Personel Başvuru Sistemi - İş Kırılım Yapısı (WBS)

## 1. Proje Kurulumu ve Temel Yapı

### 1.1. Geliştirme Ortamlarının Kurulması
- Yerel geliştirme ortamı
- Test ortamı
- Staging ortamı
- Canlı ortam

### 1.2. Versiyon Kontrol Sistemi Kurulumu
- Git repository yapılandırması
- Dallandırma (branching) stratejisi
- Code review süreci

### 1.3. CI/CD Pipeline Kurulumu
- Otomatik test
- Statik kod analizi
- Otomatik deployment

### 1.4. Frontend Projesi Temeli
- Vue.js proje yapısı
- Temel bileşenler
- Yönlendirme (routing) yapısı
- Durum yönetimi (state management)

### 1.5. Backend Projesi Temeli
- Django projesi yapısı
- REST API yapılandırması
- Veritabanı bağlantısı
- Temel middleware yapılandırması

### 1.6. Veritabanı Kurulumu
- PostgreSQL kurulumu ve yapılandırması
- İlk migrasyonlar
- Veritabanı erişim güvenliği

### 1.7. UI Kiti ve Stil Rehberi
- Tasarım sistemi
- Temel bileşenler
- Tipografi ve renk paleti

## 2. Kullanıcı Yönetimi ve Kimlik Doğrulama

### 2.1. Kullanıcı Rolleri ve Yetkilendirme
- Rol modelleri (Aday, Admin, Yönetici, Jüri)
- Yetki tanımlamaları
- Erişim kontrolü

### 2.2. Giriş Sistemi
- TC Kimlik No ve şifre ile giriş
- Şifre güvenliği
- Oturum yönetimi

### 2.3. e-Devlet Entegrasyonu
- API bağlantısı
- Kimlik doğrulama akışı
- Veri alışverişi

### 2.4. Şifre Sıfırlama
- Şifre sıfırlama e-postası
- Güvenli bağlantılar
- Şifre politikaları

### 2.5. Jüri Üyesi Kayıt Sistemi
- Yönetici tarafından ekleme
- Davet e-postası
- Hesap aktivasyonu

### 2.6. JWT Oturum Yönetimi
- Token üretimi
- Token yenileme
- Token doğrulama

## 3. İlan Yönetimi (Admin Rolü)

### 3.1. İlan Ekleme
- İlan formu
- Gerekli alanlar validasyonu
- Taslak kaydetme fonksiyonu

### 3.2. İlan Kategorileri
- Kadro türlerine göre kategoriler
- Filtreleme sistemi
- Kategori yönetimi

### 3.3. İlan Tarih Yönetimi
- Başlangıç/bitiş tarihi ayarları
- Otomatik yayınlama/sonlandırma
- Tarih doğrulama

### 3.4. Belge Şablonları
- Gerekli belge listesi tanımlama
- Belge şablonları yükleme
- Belge tipleri yönetimi

### 3.5. İlan Düzenleme
- Aktif ilanları düzenleme
- Düzenleme geçmişi
- İptal ve güncelleme işlemleri

### 3.6. İlan Durumu Yönetimi
- Aktif/Pasif durum kontrolü
- Durum değişikliği bildirimleri
- Durum geçiş kuralları

### 3.7. İlan Listeleme ve Filtreleme
- Admin paneli listesi
- Gelişmiş filtreleme
- Toplu işlemler

### 3.8. Aktif İlan Gösterimi (Ana Sayfa)
- Topluluk görünümü
- Sayfalama ve sıralama
- Arama fonksiyonu

## 4. Başvuru Süreci (Aday Rolü)

### 4.1. İlan Detay Görüntüleme
- İlan bilgileri
- Başvuru koşulları
- Gerekli belgeler

### 4.2. Başvuru Formu
- Çok adımlı form
- Kişisel bilgiler
- Eğitim bilgileri
- Akademik çalışmalar
- Belge yükleme

### 4.3. Belge Yükleme Altyapısı
- Dosya seçme ve yükleme
- Dosya tipi ve boyut kontrolü
- Depolama yönetimi

### 4.4. Form Validasyonu
- Veri doğrulama
- Zorunlu alan kontrolü
- Hata mesajları

### 4.5. Başvuru Önizleme
- Form verilerinin özeti
- Belgelerin listelenmesi
- Doğrulama ekranı

### 4.6. Başvuru Tamamlama
- Onay işlemi
- Referans numarası üretimi
- Başvuru makbuzu

### 4.7. Başvuru Takibi
- Başvuru durumu görüntüleme
- Geçmiş başvurular
- Durum güncellemeleri

## 5. Kriter Yönetimi ve Otomatik Puanlama

### 5.1. Kriter Yönetim Paneli
- Fakülte/Kadro bazlı kriterler
- Minimum puan/makale kuralları
- A1-A5 kategorileri

### 5.2. Başlıca Yazar Kuralları
- Başlıca yazar tanımlaması
- Puan hesaplama kuralları
- Özel durumlar

### 5.3. Otomatik Puan Hesaplama
- Puan algoritması
- Yüklenen verilere göre hesaplama
- Sonuç gösterimi

### 5.4. Tablo 5 Oluşturma
- Otomatik tablo formatı
- PDF çıktısı
- İndirme fonksiyonu

## 6. Değerlendirme Süreci

### 6.1. Başvuru Listeleme (Yönetici)
- Tamamlanan başvurular
- İlan bazlı gruplandırma
- İstatistikler

### 6.2. Jüri Atama
- Jüri üyesi seçimi
- Atama bildirimleri
- Atama yönetimi

### 6.3. Başvuru İnceleme (Jüri)
- Aday bilgileri görüntüleme
- Belge inceleme
- Değerlendirme notları

### 6.4. Değerlendirme Formu
- Değerlendirme kriterleri
- Zorunlu alanlar
- Rapor yükleme

### 6.5. Karar Verme
- Olumlu/Olumsuz karar
- Gerekçe bildirimi
- Onay mekanizması

### 6.6. Jüri Kararlarının Gizliliği
- Yetkilendirme kontrolü
- Veri izolasyonu
- Erişim kısıtlamaları

### 6.7. Raporların Görüntülenmesi
- Yönetici için rapor listesi
- Rapor detayları
- Toplu görüntüleme

### 6.8. Nihai Karar
- Yönetici kararı
- Onay/ret akışı
- Sonuç bildirimi

## 7. Bildirim ve Raporlama

### 7.1. E-posta Bildirimleri
- Otomatik bildirim şablonları
- Durum değişikliği bildirimleri
- E-posta gönderim altyapısı

### 7.2. Sistem İçi Bildirimler
- Bildirim merkezi
- Okundu/okunmadı durumu
- Bildirim ayarları

### 7.3. Toplu PDF İndirme
- Başvuru belgelerini paketleme
- Toplu indirme
- Dosya organizasyonu

### 7.4. İstatistik Raporları
- Başvuru istatistikleri
- Demografik veriler
- Trend analizleri

### 7.5. Jüri Raporları
- Rapor arşivi
- Dönemsel raporlar
- Arama ve filtreleme

### 7.6. Sonuç Bildirimi
- Adaylara sonuç bildirimi
- Bildirim zamanlaması
- Bildirim takibi

## 8. Güvenlik ve Performans

### 8.1. Güvenlik Önlemleri
- Yetkilendirme sistemi
- Veri şifreleme
- XSS/CSRF koruması
- SQL enjeksiyon önleme
- HTTPS yapılandırması

### 8.2. İşlem Loglama
- Kullanıcı işlem logları
- Hata logları
- Güvenlik logları

### 8.3. Performans Optimizasyonları
- Veritabanı sorgu optimizasyonu
- API yanıt süresi iyileştirmeleri
- Frontend yükleme süresi optimizasyonu

### 8.4. Veritabanı Yedekleme
- Otomatik yedekleme
- Yedekleme stratejisi
- Yedekten geri dönüş testleri

## 9. Test ve Dağıtım

### 9.1. Test Planları
- Birim testleri
- Entegrasyon testleri
- E2E testleri
- Kullanıcı kabul testleri
- Performans testleri
- Güvenlik testleri

### 9.2. Otomatik Testler
- Test otomasyonu
- Test raporlama
- Sürekli entegrasyon

### 9.3. Kullanıcı Kabul Testleri
- Test senaryoları
- Paydaş katılımı
- Geri bildirim toplama

### 9.4. Staging Ortamı
- Prodüksiyon benzeri ortam
- Data anonimleştirme
- Performans testi

### 9.5. Canlıya Geçiş
- Dağıtım planı
- Dağıtım scriptleri
- Versiyon yönetimi

### 9.6. Canlı İzleme
- Performans izleme
- Hata takibi
- Kullanım analizi

### 9.7. Acil Durum Planı
- Geri alma prosedürü
- Yedekten geri dönüş
- Kesinti yönetimi 