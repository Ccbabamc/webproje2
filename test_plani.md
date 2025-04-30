# KOÜ Akademik Personel Başvuru Sistemi - Test Planı

Bu doküman, Kocaeli Üniversitesi Akademik Personel Başvuru Sistemi'nin test stratejisi ve test süreçlerini detaylandırmaktadır.

## 1. Giriş

### 1.1. Amaç

Bu test planının amacı, Akademik Personel Başvuru Sistemi'nin tüm bileşenlerinin işlevsel gereksinimlerini karşıladığını ve beklenen kalite standartlarına uygun olduğunu doğrulamaktır.

### 1.2. Kapsam

Test planı aşağıdaki test türlerini kapsamaktadır:

- Birim Testleri
- Entegrasyon Testleri
- Sistem Testleri
- Performans Testleri
- Güvenlik Testleri
- Kullanıcı Kabul Testleri

### 1.3. Doküman Referansları

- İş Gereksinimleri Dokümanı
- Yazılım Mimari Dokümanı
- İş Kırılım Yapısı
- API Dokümantasyonu

## 2. Test Stratejisi

### 2.1. Test Seviyeleri

#### 2.1.1. Birim Testleri
- Django modellerinin birim testleri
- Servis/Yardımcı fonksiyonların birim testleri
- Vue.js bileşenlerinin birim testleri

#### 2.1.2. Entegrasyon Testleri
- Backend API entegrasyon testleri
- Frontend-Backend entegrasyon testleri
- Harici servis entegrasyon testleri (e-Devlet vb.)

#### 2.1.3. Sistem Testleri
- Uçtan uca iş akışı testleri
- Kullanıcı senaryoları testleri

#### 2.1.4. Kabul Testleri
- Kullanıcı kabul testleri (UAT)
- İş gereksinimleri doğrulama testleri

### 2.2. Test Türleri

#### 2.2.1. Fonksiyonel Testler
- Kullanıcı girişi ve rol kontrolü
- İlan yönetimi
- Başvuru işlemleri
- Değerlendirme süreci
- Bildirim sistemi

#### 2.2.2. Performans Testleri
- Yük testleri
- Stres testleri
- Dayanıklılık testleri
- Ölçeklenebilirlik testleri

#### 2.2.3. Güvenlik Testleri
- OWASP Top 10 testleri
- Kimlik doğrulama ve yetkilendirme testleri
- Veri şifreleme testleri
- Penetrasyon testleri

#### 2.2.4. Kullanılabilirlik Testleri
- Kullanıcı arayüzü testleri
- Erişilebilirlik testleri
- Tarayıcı uyumluluk testleri

#### 2.2.5. Veri Doğrulama Testleri
- Veri bütünlüğü testleri
- Veri geçerlilik kontrolü

## 3. Test Ortamları

### 3.1. Geliştirme Ortamı
- Yerel geliştirici bilgisayarları
- Geliştirme veritabanı
- Mock harici servisler

### 3.2. Test Ortamı
- Test sunucusu
- Test veritabanı
- Test kullanıcıları
- Simüle edilmiş harici servisler

### 3.3. Staging Ortamı
- Prodüksiyon benzeri yapılandırma
- Anonimleştirilmiş gerçek veri
- Staging harici servis bağlantıları

### 3.4. Prodüksiyon Ortamı
- Canlı sunucular
- Canlı veritabanı
- Gerçek harici servis bağlantıları

## 4. Test Süreçleri

### 4.1. Test Planlama

#### 4.1.1. Test Kapsamı Belirleme
- Test edilecek fonksiyonlar ve özellikler
- Test edilmeyecek alanlar
- Risk değerlendirmesi

#### 4.1.2. Test Takvimi
- Test fazları ve zaman çizelgesi
- Kilometre taşları ve teslimatlar
- Kaynak planlaması

### 4.2. Test Tasarımı

#### 4.2.1. Test Senaryoları
- Kullanıcı rolleri bazında test senaryoları
- İş akışları bazında test senaryoları
- Hata durumları için test senaryoları

#### 4.2.2. Test Verileri
- Test verisi oluşturma stratejisi
- Test verisi yönetimi

### 4.3. Test Yürütme

#### 4.3.1. Test Koşumu
- Manuel test koşumu prosedürleri
- Otomatik test koşumu prosedürleri
- Sürekli entegrasyon test koşumu

#### 4.3.2. Hata Raporlama
- Hata sınıflandırma
- Hata takibi
- Hata çözümleme süreci

### 4.4. Test Raporlama

#### 4.4.1. Test İlerleme Raporları
- Günlük test ilerleme raporları
- Haftalık test özet raporları

#### 4.4.2. Test Tamamlama Raporu
- Test sonuçları özeti
- Bulunan hatalar ve çözüm durumları
- Öneriler ve sonraki adımlar

## 5. Test Otomasyonu

### 5.1. Otomasyon Stratejisi
- Otomatikleştirilecek test senaryoları
- Otomasyon araçları ve çerçeveleri
- Otomasyon mimarisi

### 5.2. Otomasyon Araçları
- Birim test araçları: pytest, Jest
- API test araçları: Postman, pytest-django
- UI test araçları: Cypress, Selenium
- Performans test araçları: JMeter, Locust
- Sürekli entegrasyon araçları: Jenkins, GitHub Actions

### 5.3. Otomasyon Planı
- Otomasyon önceliklendirilmesi
- Otomasyon uygulama takvimi
- Otomasyon bakım stratejisi

## 6. Test Verileri

### 6.1. Test Veri Gereksinimleri
- Fakülte ve bölüm verileri
- Kullanıcı verileri
- İlan verileri
- Başvuru verileri
- Değerlendirme verileri

### 6.2. Test Veri Yönetimi
- Test verisi oluşturma yöntemleri
- Test verisi bakımı
- Veri gizliliği ve anonimleştirme

## 7. Detaylı Test Senaryoları

### 7.1. Kullanıcı Yönetimi Testleri

| Test ID | Senaryo | Açıklama | Önkoşullar | Beklenen Sonuç |
|---------|---------|----------|------------|----------------|
| UT-001  | Kullanıcı Kaydı | Yeni aday kaydı | - | Kullanıcı başarıyla kaydedilir |
| UT-002  | Kullanıcı Girişi | TC Kimlik No ve şifre ile giriş | Kayıtlı kullanıcı | Başarılı giriş |
| UT-003  | Şifre Sıfırlama | Şifre sıfırlama süreci | Kayıtlı kullanıcı | Şifre başarıyla sıfırlanır |
| UT-004  | e-Devlet Doğrulama | e-Devlet ile kullanıcı doğrulama | Kayıtlı kullanıcı | Başarılı doğrulama |
| UT-005  | Profil Güncelleme | Kullanıcı profil bilgileri güncelleme | Giriş yapmış kullanıcı | Profil güncellenir |

### 7.2. İlan Yönetimi Testleri

| Test ID | Senaryo | Açıklama | Önkoşullar | Beklenen Sonuç |
|---------|---------|----------|------------|----------------|
| AT-001  | İlan Oluşturma | Admin tarafından yeni ilan oluşturma | Admin kullanıcı girişi | İlan oluşturulur |
| AT-002  | İlan Düzenleme | Mevcut ilanı düzenleme | Admin kullanıcı, mevcut ilan | İlan güncellenir |
| AT-003  | İlan Yayınlama | Taslak ilanı yayınlama | Admin kullanıcı, taslak ilan | İlan yayınlanır |
| AT-004  | İlan Kapatma | Aktif ilanı kapatma | Admin kullanıcı, aktif ilan | İlan kapatılır |
| AT-005  | İlan Filtreleme | İlanları kriterlere göre filtreleme | İlanlar mevcut | Doğru filtre sonuçları |

### 7.3. Başvuru Testleri

| Test ID | Senaryo | Açıklama | Önkoşullar | Beklenen Sonuç |
|---------|---------|----------|------------|----------------|
| APP-001 | Başvuru Formu | Başvuru formunu doldurma | Aday girişi, aktif ilan | Form kaydedilir |
| APP-002 | Belge Yükleme | Belgeleri yükleme | Aday girişi, başlamış başvuru | Belgeler yüklenir |
| APP-003 | Başvuru Önizleme | Başvuru özetini görüntüleme | Doldurulmuş başvuru | Önizleme görüntülenir |
| APP-004 | Başvuru Tamamlama | Başvuruyu tamamlama | Tüm belgeler ve bilgiler eklenmiş | Başvuru tamamlanır |
| APP-005 | Başvuru Takibi | Başvuru durumunu kontrol etme | Tamamlanmış başvuru | Durum görüntülenir |

### 7.4. Değerlendirme Testleri

| Test ID | Senaryo | Açıklama | Önkoşullar | Beklenen Sonuç |
|---------|---------|----------|------------|----------------|
| EVL-001 | Jüri Atama | Başvuruya jüri atama | Yönetici girişi, tamamlanmış başvuru | Jüri atanır |
| EVL-002 | Başvuru İnceleme | Jürinin başvuruyu incelemesi | Jüri girişi, atanmış başvuru | İnceleme kaydedilir |
| EVL-003 | Değerlendirme Raporu | Değerlendirme raporu yükleme | Jüri girişi, incelenmiş başvuru | Rapor yüklenir |
| EVL-004 | Nihai Karar | Yöneticinin nihai kararı | Yönetici girişi, değerlendirilmiş başvuru | Karar kaydedilir |
| EVL-005 | Sonuç Bildirimi | Adaya sonuç bildirimi | Karar verilmiş başvuru | Bildirim gönderilir |

### 7.5. Performans Testleri

| Test ID | Senaryo | Açıklama | Önkoşullar | Beklenen Sonuç |
|---------|---------|----------|------------|----------------|
| PERF-001 | Ana Sayfa Yüklenmesi | Ana sayfa yüklenme süresi | - | <2 saniye |
| PERF-002 | İlan Listeleme | İlanları listeleme süresi | İlanlar mevcut | <3 saniye |
| PERF-003 | Başvuru Gönderimi | Başvuru gönderme işlem süresi | Doldurulmuş başvuru | <5 saniye |
| PERF-004 | Eşzamanlı Kullanıcı | 50 eşzamanlı kullanıcı ile performans | Test ortamı | Normal işleyiş |
| PERF-005 | Yük Testi | 1000 başvuru ile sistem performansı | Test ortamı | Kabul edilebilir yanıt süreleri |

### 7.6. Güvenlik Testleri

| Test ID | Senaryo | Açıklama | Önkoşullar | Beklenen Sonuç |
|---------|---------|----------|------------|----------------|
| SEC-001 | XSS Koruması | Cross-site scripting koruması | - | XSS saldırıları engellenir |
| SEC-002 | SQL Enjeksiyon | SQL enjeksiyonu test senaryoları | - | SQL enjeksiyonları engellenir |
| SEC-003 | CSRF Koruması | Cross-site request forgery koruması | - | CSRF saldırıları engellenir |
| SEC-004 | Yetki Kontrolü | Yetkisiz erişim denemeleri | Farklı rol kullanıcıları | Yetkisiz erişimler engellenir |
| SEC-005 | Veri Şifreleme | Hassas verilerin şifrelenmesi | - | Veriler şifrelenir |

## 8. Test Teslim Kriterleri

### 8.1. Genel Teslim Kriterleri
- Kritik hataların sıfır olması
- Yüksek öncelikli hataların maksimum 5 olması
- Tüm kullanıcı kabul testlerinin geçmesi
- Performans kriterlerinin karşılanması
- Güvenlik açıklarının giderilmesi

### 8.2. Modül Bazlı Teslim Kriterleri
- Kullanıcı Yönetimi: %100 test başarısı
- İlan Yönetimi: %95 test başarısı
- Başvuru Süreci: %95 test başarısı
- Değerlendirme Süreci: %95 test başarısı
- Bildirim Sistemi: %90 test başarısı

## 9. Test Ekibi ve Sorumluluklar

### 9.1. Test Ekibi
- Test Lideri
- Fonksiyonel Test Uzmanları (2 kişi)
- Performans Test Uzmanı
- Güvenlik Test Uzmanı
- Otomasyon Test Uzmanı

### 9.2. Sorumluluklar
- Test Lideri: Test planlaması, koordinasyon, raporlama
- Fonksiyonel Test Uzmanları: Manuel testler, test senaryoları
- Performans Test Uzmanı: Yük, stres ve performans testleri
- Güvenlik Test Uzmanı: Güvenlik açıklarını test etme
- Otomasyon Test Uzmanı: Test otomasyonu geliştirme

## 10. Risk ve Sorun Yönetimi

### 10.1. Test Riskleri
- Test ortamı hazırlık gecikmeleri
- Test verisi hazırlık sorunları
- Test ekibi kaynak yetersizliği
- Test otomasyonu zorlukları
- Beklenmeyen hata yoğunluğu

### 10.2. Risk Azaltma Stratejileri
- Erken test ortamı hazırlığı
- Test verisi kütüphanesi oluşturma
- Yedek kaynak planlaması
- Aşamalı otomasyon stratejisi
- Sık geri bildirim döngüleri

## 11. Ekler

### 11.1. Test Kontrol Listeleri
- Birim test kontrol listesi
- Entegrasyon test kontrol listesi
- Kullanıcı arayüzü test kontrol listesi

### 11.2. Test Şablonları
- Hata raporu şablonu
- Test senaryo şablonu
- Test raporu şablonu

## 12. Onay

| İsim | Pozisyon | Tarih | İmza |
|------|----------|-------|------|
|      | Test Lideri |     |      |
|      | Proje Yöneticisi |     |      |
|      | Yazılım Geliştirme Lideri |     |      | 