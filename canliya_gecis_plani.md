# KOÜ Akademik Personel Başvuru Sistemi - Canlıya Geçiş Planı

Bu doküman, Kocaeli Üniversitesi Akademik Personel Başvuru Sistemi'nin geliştirme ortamından canlı ortama geçiş sürecini detaylandırmaktadır.

## 1. Genel Bakış

Canlıya geçiş, aşağıdaki aşamalardan oluşacaktır:

1. Ön Hazırlık ve Planlama
2. Altyapı Hazırlığı
3. Uygulama Dağıtımı
4. Test ve Doğrulama
5. Veri Göçü
6. Son Kullanıcı Eğitimi
7. Canlıya Geçiş
8. İzleme ve Stabilizasyon
9. Dokümantasyon ve Bilgi Aktarımı

## 2. Zaman Çizelgesi

| Aşama | Faaliyet | Sorumlu | Başlangıç | Bitiş | Durum |
|-------|----------|---------|-----------|-------|-------|
| 1 | Canlıya geçiş planı onayı | Proje Yöneticisi | T-30 | T-28 | |
| 1 | Risk analizi tamamlanması | Proje Yöneticisi + Teknik Ekip | T-28 | T-25 | |
| 2 | Sunucu yapılandırması | DevOps/BT Ekibi | T-25 | T-20 | |
| 2 | Veritabanı kurulumu | DevOps/BT Ekibi | T-22 | T-18 | |
| 2 | Ağ yapılandırması | DevOps/BT Ekibi | T-20 | T-15 | |
| 2 | Güvenlik yapılandırması | DevOps/BT Ekibi | T-18 | T-15 | |
| 3 | Backend dağıtımı | DevOps/Geliştirme Ekibi | T-15 | T-13 | |
| 3 | Frontend dağıtımı | DevOps/Geliştirme Ekibi | T-13 | T-11 | |
| 4 | Fonksiyonel testler | Test Ekibi | T-10 | T-8 | |
| 4 | Performans testleri | Test Ekibi | T-9 | T-7 | |
| 4 | Güvenlik testleri | Test Ekibi | T-8 | T-6 | |
| 5 | Referans verilerinin yüklenmesi | Veri Analisti + BT Ekibi | T-7 | T-5 | |
| 6 | Admin eğitimi | Eğitim Ekibi | T-14 | T-10 | |
| 6 | Yönetici eğitimi | Eğitim Ekibi | T-10 | T-7 | |
| 6 | Jüri üyesi eğitimi | Eğitim Ekibi | T-7 | T-4 | |
| 7 | Go/No-Go kararı | Tüm paydaşlar | T-2 | T-2 | |
| 7 | Canlı yayına alma | DevOps/BT Ekibi | T | T | |
| 8 | Hypercare izleme | Geliştirme Ekibi + BT Ekibi | T | T+14 | |
| 9 | İşletim dokümantasyonu | Dokümantasyon Ekibi | T-20 | T-5 | |

*T: Canlıya geçiş tarihi, T-X: Canlıya geçişten X gün önce, T+X: Canlıya geçişten X gün sonra*

## 3. Aşama Detayları

### 3.1. Ön Hazırlık ve Planlama

#### 3.1.1. Canlıya Geçiş Ekibinin Oluşturulması
- Proje Yöneticisi (Koordinasyon)
- DevOps/Sistem Uzmanı (Altyapı)
- Veritabanı Uzmanı
- Frontend Geliştirici
- Backend Geliştirici
- Test Uzmanı
- BT Destek Personeli
- Dokümantasyon Sorumlusu

#### 3.1.2. Rollerin ve Sorumlulukların Belirlenmesi
- Her ekip üyesinin görev tanımı
- İletişim kanalları ve eskalasyon prosedürleri
- Acil durum iletişim listesi

#### 3.1.3. Risk Analizi ve Acil Durum Planı
- Olası risklerin tespit edilmesi
- Risk azaltma stratejileri
- Geri alma (rollback) planı
- Felaket kurtarma planı

### 3.2. Altyapı Hazırlığı

#### 3.2.1. Sunucu Altyapısı
- Üretim sunucularının kurulumu (Fiziksel veya Sanal)
- İşletim sistemi optimizasyonu
- Sunucu güvenliği yapılandırması
- Yedekleme sisteminin kurulumu

#### 3.2.2. Veritabanı Ortamı
- PostgreSQL veritabanı kurulumu
- Veritabanı yapılandırması ve optimizasyonu
- Yedekleme ve kurtarma prosedürleri
- Replikasyon (gerekli ise)

#### 3.2.3. Ağ Yapılandırması
- Firewall kuralları
- Ağ segmentasyonu
- Load balancer (yük dengeleyici) kurulumu (gerekli ise)
- SSL sertifikası kurulumu

#### 3.2.4. Monitoring ve Logging
- Uygulama performans izleme araçları
- Sunucu izleme araçları
- Merkezi log yönetimi
- Alarm ve bildirim sistemi

### 3.3. Uygulama Dağıtımı

#### 3.3.1. Backend Dağıtımı
- Kod deposundan üretim versiyonunun alınması
- Üretim ortamı için `.env` dosyasının hazırlanması
- Django uygulamasının dağıtımı
- Gunicorn ve Nginx yapılandırması

#### 3.3.2. Frontend Dağıtımı
- Vue.js uygulamasının derlemesi (build)
- Statik dosyaların Nginx ile sunulması
- CDN (içerik dağıtım ağı) yapılandırması (gerekli ise)

#### 3.3.3. Entegrasyon Noktaları
- e-Devlet entegrasyonu
- E-posta sistemi entegrasyonu
- Diğer KOÜ sistemleriyle entegrasyon (gerekli ise)

### 3.4. Test ve Doğrulama

#### 3.4.1. Fonksiyonel Testler
- Tüm kullanıcı rolleri için kritik iş akışları
- Form validasyonları
- Dosya yükleme/indirme işlemleri
- Bildirim mekanizmaları

#### 3.4.2. Performans Testleri
- Yük testleri (eşzamanlı kullanıcı senaryoları)
- Stres testleri
- Veritabanı performans testleri
- Sayfa yüklenme süreleri

#### 3.4.3. Güvenlik Testleri
- OWASP Top 10 zafiyet taraması
- Kimlik doğrulama ve yetkilendirme testleri
- Veri şifreleme kontrolü
- API güvenlik testleri

#### 3.4.4. Geçiş Kriterleri
- Tüm kritik fonksiyonlar çalışıyor
- Performans eşik değerleri karşılanıyor
- Güvenlik açıkları giderilmiş
- Tüm entegrasyonlar doğrulanmış

### 3.5. Veri Göçü

#### 3.5.1. Referans Verilerinin Hazırlanması
- Fakülte verileri
- Bölüm verileri
- Akademik pozisyon verileri
- Kriter tanımları
- Dokümantasyon şablonları

#### 3.5.2. Test Verileri Temizliği
- Staging/test ortamından üretim ortamına geçiş sürecinde test verilerinin temizlenmesi

#### 3.5.3. İlk Admin Kullanıcıların Oluşturulması
- Sistem yöneticisi hesapları
- Fakülte/bölüm yöneticisi hesapları

### 3.6. Son Kullanıcı Eğitimi

#### 3.6.1. Eğitim Programları
- Admin kullanıcıları için eğitim
- Yönetici kullanıcıları için eğitim
- Jüri üyeleri için eğitim

#### 3.6.2. Eğitim Materyalleri
- Kullanıcı kılavuzları
- Eğitim videoları
- Sık sorulan sorular (SSS)

#### 3.6.3. Destek Mekanizması
- Destek masası/yardım hattı kurulumu
- Sorun bildirim prosedürü

### 3.7. Canlıya Geçiş

#### 3.7.1. Go/No-Go Toplantısı
- Tüm paydaşların katılımı
- Canlıya geçiş kriterlerinin değerlendirilmesi
- Son acil durum planı gözden geçirme
- İmza/onay süreci

#### 3.7.2. Canlıya Alma Prosedürü
- Canlıya geçiş sırasında detaylı görev listesi
- Zaman çizelgesi
- İletişim kanalları
- Kontrol listesi

#### 3.7.3. İlk Kullanıcı Erişimi
- Aşamalı kullanıcı erişimi planı
- İlk kullanıcı deneyimi izleme

### 3.8. İzleme ve Stabilizasyon

#### 3.8.1. Hypercare Dönemi
- Canlıya geçiş sonrası ilk 2 hafta için yoğun izleme
- Acil durum müdahale ekibi hazır bulunması
- 7/24 teknik destek (gerekli ise)

#### 3.8.2. Performans İzleme
- Sistem performansı izleme
- Veritabanı performansı izleme
- Ağ trafiği izleme
- Kullanıcı deneyimi izleme (sayfa yüklenme süreleri vb.)

#### 3.8.3. Hata Yönetimi
- Hata raporlama ve takip
- Öncelik belirleme
- Acil düzeltme planı
- Düzenli durum raporları

### 3.9. Dokümantasyon ve Bilgi Aktarımı

#### 3.9.1. Teknik Dokümantasyon
- Sistem mimarisi
- Veritabanı şeması
- API dokümantasyonu
- Kod dokümantasyonu

#### 3.9.2. İşletim Dokümantasyonu
- Sistem yönetimi prosedürleri
- Yedekleme ve kurtarma prosedürleri
- İzleme ve hata giderme prosedürleri
- Düzenli bakım kontrol listesi

#### 3.9.3. Kullanıcı Dokümantasyonu
- Son kullanıcı kılavuzları
- Sık sorulan sorular
- Video eğitimler
- Yardım sistemi içerikleri

## 4. Risk Yönetimi

### 4.1. Olası Riskler ve Azaltma Stratejileri

| Risk | Olasılık | Etki | Azaltma Stratejisi |
|------|----------|------|---------------------|
| Sunucu donanım arızası | Düşük | Yüksek | Yedekli sunucu altyapısı, otomatik failover |
| Veritabanı erişim sorunları | Orta | Yüksek | Veritabanı replikasyonu, otomatik backup |
| Yüksek kullanıcı yükü | Orta | Orta | Load balancing, otomatik ölçeklendirme |
| Entegrasyon hataları | Yüksek | Orta | Kapsamlı entegrasyon testleri, alternatif iş akışları |
| Güvenlik ihlalleri | Düşük | Kritik | Güvenlik duvarı, düzenli güvenlik taraması, anomali tespiti |
| Hatalı veri | Orta | Yüksek | Veri doğrulama, geri alma prosedürleri |
| Uyumluluk sorunları | Orta | Orta | Tarayıcı ve cihaz uyumluluk testleri |

### 4.2. Geri Alma (Rollback) Planı

Canlıya geçiş sırasında veya sonrasında kritik sorunlar meydana gelirse aşağıdaki geri alma prosedürü uygulanacaktır:

1. **Karar Verme Süreci**
   - Geri alma kararı için yetkilendirme
   - Tetikleyici olayların tanımlanması
   - Acil durum iletişim protokolü

2. **Teknik Geri Alma Prosedürü**
   - Veritabanı geri yükleme
   - Uygulama dağıtımı geri alma
   - DNS/yönlendirme değişiklikleri

3. **İletişim Planı**
   - Kullanıcı bilgilendirme süreci
   - Paydaş iletişimi
   - Zaman çizelgesi ve beklentiler yönetimi

## 5. İletişim Planı

### 5.1. İletişim Kanalları
- Acil durum iletişimi: Telefon zinciri
- Proje durumu güncellemeleri: E-posta ve proje yönetim aracı
- Teknik ekip iletişimi: Anlık mesajlaşma (Slack/Teams)
- Paydaş bilgilendirmesi: Resmi e-posta ve toplantılar

### 5.2. Raporlama Takvimi
- Günlük durum raporu (canlıya geçiş haftası)
- Haftalık durum raporu (stabilizasyon dönemi)
- Olay raporlaması (gerektiğinde)
- Final başarı raporu (canlıya geçişten 30 gün sonra)

## 6. Kontrol Listeleri

### 6.1. Canlıya Geçiş Öncesi Kontrol Listesi
- [ ] Tüm kritik fonksiyonel testler tamamlandı
- [ ] Performans kabul kriterleri karşılandı
- [ ] Güvenlik taramaları yapıldı ve açıklar giderildi
- [ ] Veritabanı şeması ve veriler hazır
- [ ] Yedekleme ve geri yükleme prosedürleri test edildi
- [ ] Acil durum planı hazır
- [ ] İzleme araçları kuruldu ve çalışıyor
- [ ] Kullanıcı eğitimleri tamamlandı
- [ ] Teknik ekip 7/24 destek için hazır
- [ ] Tüm dokümantasyon hazır
- [ ] Go/No-Go toplantısında onay alındı

### 6.2. Canlıya Geçiş Günü Kontrol Listesi
- [ ] Tüm ekip üyeleri pozisyonda
- [ ] İletişim kanalları açık ve test edildi
- [ ] Son yedekleme alındı
- [ ] DNS yapılandırması hazır
- [ ] SSL sertifikaları aktif
- [ ] Veritabanı bağlantıları kontrol edildi
- [ ] İzleme sistemleri aktif
- [ ] Bildirim sistemleri test edildi
- [ ] Smoke testleri başarılı

### 6.3. Canlıya Geçiş Sonrası Kontrol Listesi
- [ ] Tüm kullanıcı rolleriyle temel fonksiyonlar test edildi
- [ ] İlk kullanıcı erişimi sorunsuz
- [ ] Performans izleme sonuçları normal
- [ ] Hata logları kontrol edildi
- [ ] Veritabanı performansı normal
- [ ] Entegrasyonlar düzgün çalışıyor
- [ ] Otomatik yedeklemeler programlandı
- [ ] Güvenlik izleme aktif
- [ ] Destek ekibi hazır

## 7. Onay Süreci

### 7.1. Hazırlayan

| İsim | Pozisyon | Tarih | İmza |
|------|----------|-------|------|
|      |          |       |      |

### 7.2. Onaylayan

| İsim | Pozisyon | Tarih | İmza |
|------|----------|-------|------|
|      |          |       |      |
|      |          |       |      |
|      |          |       |      | 