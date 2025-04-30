# KOÜ Akademik Personel Başvuru Sistemi - Güvenlik Politikaları

Bu doküman, Kocaeli Üniversitesi Akademik Personel Başvuru Sistemi'nin güvenlik politikalarını ve uygulamalarını detaylandırmaktadır.

## 1. Amaç ve Kapsam

### 1.1. Amaç

Bu politikanın amacı, Akademik Personel Başvuru Sistemi'nin veri güvenliğini sağlamak, gizliliğini korumak ve sistemin bütünlüğünü muhafaza etmektir. Sistem üzerinde işlenen kişisel ve kurumsal verilerin korunması için gerekli güvenlik önlemlerini tanımlamaktadır.

### 1.2. Kapsam

Bu politika aşağıdaki kapsamı içermektedir:

- Uygulama seviyesi güvenlik önlemleri
- Veritabanı güvenliği
- Ağ güvenliği
- Sunucu güvenliği
- Kimlik doğrulama ve yetkilendirme
- Şifre yönetimi
- Kişisel verilerin korunması
- Güvenlik olayları yönetimi
- İş sürekliliği

### 1.3. Hedef Kitle

- Sistem yöneticileri
- Yazılım geliştiriciler
- Veritabanı yöneticileri
- Sistem kullanıcıları (adaylar, jüri üyeleri, yöneticiler)
- BT destek personeli

## 2. Roller ve Sorumluluklar

### 2.1. Veri Sorumlusu

- Kişisel verilerin işlenmesinden sorumludur.
- KVKK ve ilgili mevzuatlara uygunluğu sağlar.
- Veri güvenliği politikalarının oluşturulmasını ve uygulanmasını gözetir.

### 2.2. Sistem Yöneticisi

- Sistem güvenliğinin sağlanmasından ve izlenmesinden sorumludur.
- Güvenlik yamalarının uygulanmasını sağlar.
- Kullanıcı hesaplarını ve yetkilerini yönetir.
- Güvenlik olaylarını izler ve müdahale eder.

### 2.3. Yazılım Geliştirme Ekibi

- Güvenli kod geliştirme prensiplerini uygular.
- Güvenlik açıklarını tespit eder ve giderir.
- Kod incelemelerini güvenlik odaklı yapar.
- Güvenlik testlerini uygular.

### 2.4. Kullanıcılar

- Şifre güvenliği kurallarına uyar.
- Şüpheli durumları raporlar.
- Sistem kullanım politikalarına uygun hareket eder.
- Kendi hesap bilgilerinin güvenliğinden sorumludur.

## 3. Uygulama Seviyesi Güvenlik

### 3.1. Güvenli Kodlama Standartları

- OWASP (Open Web Application Security Project) güvenli kodlama standartları izlenir.
- Kod incelemeleri güvenlik odaklı yapılır.
- Statik kod analizi araçları kullanılır.
- Düzenli güvenlik taramaları yapılır.

### 3.2. Giriş Doğrulama ve Sanitizasyon

- Tüm kullanıcı girdileri doğrulanır ve sanitize edilir.
- XSS (Cross-site Scripting) saldırılarına karşı koruma sağlanır.
- SQL enjeksiyonlarına karşı parametreli sorgular kullanılır.
- Sunucu tarafında veri doğrulama yapılır.

### 3.3. CSRF (Cross-Site Request Forgery) Koruması

- Django'nun yerleşik CSRF koruması aktif edilir.
- Tüm POST, PUT, DELETE işlemleri için CSRF token doğrulaması yapılır.
- Giriş yapıldığında CSRF token yenilenir.

### 3.4. XSS (Cross-Site Scripting) Koruması

- Content-Security-Policy (CSP) başlıkları kullanılır.
- Auto-escaping Template sistemi kullanılır.
- Kullanıcı içeriğinde HTML ve JavaScript filtrelenir.
- HttpOnly ve Secure bayraklı çerezler kullanılır.

### 3.5. Dosya Yükleme Güvenliği

- Yüklenen dosyaların tipi ve boyutu kontrol edilir.
- Dosyalar orijinal isimlerinden farklı rastgele isimlerle saklanır.
- Yüklenen dosyalar anti-virüs taramasından geçirilir.
- Dosya çalıştırma engellenir, sadece görüntüleme izni verilir.

### 3.6. Güvenli API Yapılandırması

- API istekleri için rate-limiting uygulanır.
- API anahtarları ve erişim tokenları güvenli şekilde saklanır.
- API'ler için yetkilendirme ve doğrulama mekanizmaları uygulanır.
- API dokümantasyonu hassas bilgiler içermez.

## 4. Kimlik Doğrulama ve Yetkilendirme

### 4.1. Kimlik Doğrulama Mekanizmaları

- TC Kimlik No ve şifre kombinasyonu kullanılır.
- e-Devlet entegrasyonu üzerinden kimlik doğrulama yapılır.
- Başarısız giriş denemeleri sınırlandırılır ve izlenir.
- JWT (JSON Web Token) tabanlı oturum yönetimi kullanılır.

### 4.2. Şifre Politikaları

- Şifreler en az 8 karakter uzunluğunda olmalıdır.
- Şifre içerisinde en az bir büyük harf, bir küçük harf, bir rakam ve bir özel karakter bulunmalıdır.
- Şifreler her 90 günde bir değiştirilmelidir.
- Son 5 şifre tekrar kullanılamaz.
- Varsayılan veya tahmin edilebilir şifreler kabul edilmez.

### 4.3. Çok Faktörlü Kimlik Doğrulama

- Kritik işlemler için SMS veya e-posta ile doğrulama kodu gönderilir.
- Yönetici hesapları için çok faktörlü kimlik doğrulama zorunludur.
- Yeni cihazdan giriş yapıldığında ek doğrulama istenir.

### 4.4. Rol Tabanlı Erişim Kontrolü

- Sistemde 4 ana rol tanımlanmıştır: Aday, Admin, Yönetici, Jüri.
- Her rol için ayrı yetki setleri tanımlanmıştır.
- En az ayrıcalık prensibi uygulanır.
- Yetki değişiklikleri loglanır ve izlenir.

### 4.5. Oturum Yönetimi

- Oturum süresi 30 dakika ile sınırlandırılmıştır, ardından timeout olur.
- Her oturum için benzersiz oturum kimliği oluşturulur.
- Oturum bilgileri şifrelenir ve güvenli çerezlerde saklanır.
- Çıkış yapıldığında oturum tamamen sonlandırılır.

## 5. Veri Güvenliği ve Gizliliği

### 5.1. Kişisel Verilerin Korunması

- 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) hükümlerine tam uyum sağlanır.
- Kullanıcılar, hangi verilerinin toplandığı ve nasıl kullanıldığı konusunda bilgilendirilir.
- Veri işleme amaçları açıkça belirtilir ve kullanıcıdan açık rıza alınır.
- Kişisel veriler, işlenme amacı sona erdiğinde silinir veya anonimleştirilir.

### 5.2. Veri Şifreleme

- Hassas veriler veritabanında şifrelenmiş olarak saklanır (TC Kimlik No, belge içerikleri).
- İletişim TLS/SSL ile şifrelenir (HTTPS zorunludur).
- Dosya sistemi şifrelemesi uygulanır.
- Şifreleme anahtarları güvenli bir şekilde yönetilir.

### 5.3. Veri Tabanı Güvenliği

- Veritabanı sunucusu ayrı bir güvenlik katmanında bulunur.
- Veritabanı erişimi rol bazlı sınırlandırılmıştır.
- Veritabanı sorguları parametreli olarak yapılır.
- Veritabanı yedekleri şifrelenir ve güvenli şekilde saklanır.

### 5.4. Veri Sınıflandırması

- Veriler hassasiyet derecesine göre sınıflandırılır (gizli, hassas, dahili, genel).
- Her veri sınıfı için uygun koruma önlemleri uygulanır.
- Hassas verilere erişim kısıtlıdır ve loglanır.
- Veri sınıflandırması düzenli olarak gözden geçirilir.

### 5.5. Veri Bütünlüğü

- Verilerin yetkisiz değiştirilmesini önlemek için bütünlük kontrolleri yapılır.
- Belgelerin hash değerleri saklanır ve doğrulanır.
- Değişiklik yapılabilen veriler için değişiklik geçmişi tutulur.
- Kritik verilerde yapılan değişiklikler için onay mekanizmaları uygulanır.

## 6. Ağ ve Altyapı Güvenliği

### 6.1. Ağ Segmentasyonu

- Uygulama, veritabanı ve yönetim katmanları ayrı ağ segmentlerinde bulunur.
- İç ağ ve dış ağ arasında güvenlik duvarı bulunur.
- Ağlar arası erişim kontrolü uygulanır.
- DMZ (Demilitarized Zone) yapılandırması kullanılır.

### 6.2. Güvenlik Duvarı Yapılandırması

- Web Application Firewall (WAF) yapılandırılır.
- Sadece gerekli portlar açık tutulur.
- Gelen ve giden trafik filtrelenir.
- Düzenli güvenlik duvarı kuralları gözden geçirme yapılır.

### 6.3. Güvenli İletişim

- Tüm HTTP trafiği HTTPS'e yönlendirilir.
- TLS 1.2 veya daha yüksek sürümler kullanılır.
- Güçlü şifreleme paketleri tercih edilir.
- HTTP Strict Transport Security (HSTS) uygulanır.

### 6.4. DDoS Koruması

- DDoS (Distributed Denial of Service) saldırılarına karşı koruma sağlanır.
- Anormal trafik örüntüleri izlenir.
- Rate limiting uygulanır.
- CDN hizmetleri kullanılır.

## 7. Sunucu Güvenliği

### 7.1. İşletim Sistemi Güvenliği

- Sunucu işletim sistemleri güvenli yapılandırılır.
- Gerekli olmayan servisler ve portlar kapatılır.
- Düzenli güvenlik yamaları uygulanır.
- Sıkılaştırma (hardening) prosedürleri uygulanır.

### 7.2. Güncelleme Yönetimi

- Kritik güvenlik yamaları 24 saat içinde uygulanır.
- Düzenli yazılım güncellemeleri yapılır.
- Yama yönetimi politikası uygulanır.
- Yama uygulaması öncesi test edilir.

### 7.3. Anti-Virüs ve Kötü Amaçlı Yazılım Koruması

- Sunucularda anti-virüs yazılımları kullanılır.
- Düzenli virüs taramaları yapılır.
- Virüs imzaları güncel tutulur.
- Davranış bazlı kötü amaçlı yazılım tespiti yapılır.

### 7.4. Otomasyon ve Yapılandırma Yönetimi

- Sunucu yapılandırmaları otomatize edilir ve versiyonlanır.
- Değişiklik yönetimi süreçleri uygulanır.
- Infrastructure as Code prensipleri kullanılır.
- Yapılandırma sapmaları izlenir ve düzeltilir.

## 8. İzleme, Log Yönetimi ve Olay Müdahalesi

### 8.1. Log Yönetimi

- Tüm sistem ve uygulama logları merkezi olarak toplanır.
- Loglar en az 2 yıl süreyle saklanır.
- Loglar değiştirilemez ve silinemezcşekilde depolanır.
- Erişim, güvenlik, sistem ve uygulama logları tutulur.

### 8.2. Güvenlik İzleme

- Güvenlik olayları gerçek zamanlı izlenir.
- Anormal davranışlar için uyarı mekanizmaları kurulur.
- Güvenlik bilgi ve olay yönetimi (SIEM) sistemi kullanılır.
- Kritik sistemler 7/24 izlenir.

### 8.3. Olay Müdahalesi

- Güvenlik olayları için resmi müdahale prosedürleri tanımlanmıştır.
- Olay müdahale ekibi ve sorumlulukları belirlenmiştir.
- Olay sınıflandırma ve önceliklendirme yapılır.
- İletişim kanalları ve eskalasyon süreçleri tanımlanmıştır.

### 8.4. Adli Analiz

- Güvenlik ihlallerinde adli analiz için kanıt toplama prosedürleri uygulanır.
- Dijital kanıtların bütünlüğü korunur.
- Olay soruşturma süreci belgelendirilir.
- Yasal gereklilikler takip edilir.

## 9. İş Sürekliliği ve Felaket Kurtarma

### 9.1. Yedekleme Stratejisi

- Veritabanı günlük tam yedeklenir, saatlik artımlı yedekleme yapılır.
- Uygulama kodu ve yapılandırmaları versiyonlanır ve yedeklenir.
- Yedekler şifrelenir ve çevrimdışı olarak da saklanır.
- Yedekleme ve geri yükleme testleri düzenli olarak yapılır.

### 9.2. Felaket Kurtarma Planı

- Farklı felaket senaryoları için kurtarma planları tanımlanmıştır.
- Kurtarma süresi hedefleri (RTO) ve Kurtarma noktası hedefleri (RPO) belirlenmiştir.
- Alternatif veri merkezi ve sistemler hazırlanmıştır.
- Yılda en az bir kez felaket kurtarma tatbikatı yapılır.

### 9.3. İş Sürekliliği Planı

- Kritik iş süreçleri ve bağımlılıkları tanımlanmıştır.
- Kesinti durumunda alternatif iş süreçleri belirlenmiştir.
- İletişim planları ve sorumluluklar tanımlanmıştır.
- Düzenli iş sürekliliği tatbikatları yapılır.

## 10. Uyum ve Denetim

### 10.1. Yasal Uyum

- 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK)
- 5651 sayılı İnternet Ortamında Yapılan Yayınların Düzenlenmesi ve Bu Yayınlar Yoluyla İşlenen Suçlarla Mücadele Edilmesi Hakkında Kanun
- Elektronik İmza Kanunu ve ilgili mevzuatlar
- Yükseköğretim Kurumu (YÖK) düzenlemeleri

### 10.2. Güvenlik Değerlendirmeleri ve Denetimler

- Yılda en az bir kez iç güvenlik denetimi yapılır.
- 2 yılda bir bağımsız dış güvenlik denetimi yaptırılır.
- Zafiyet taramaları 3 ayda bir gerçekleştirilir.
- Penetrasyon testleri yılda bir kez yapılır.

### 10.3. Politika İnceleme ve Güncelleme

- Güvenlik politikaları yılda en az bir kez gözden geçirilir.
- Güvenlik politikalarında yapılan değişiklikler belgelendirilir.
- Politika değişiklikleri tüm ilgili paydaşlara duyurulur.
- Politika uyumu düzenli olarak kontrol edilir.

## 11. Eğitim ve Farkındalık

### 11.1. Güvenlik Eğitimleri

- Tüm sistem yöneticileri ve geliştiriciler yılda en az 20 saat güvenlik eğitimi alır.
- Yeni işe alınan personel işe başlamadan önce temel güvenlik eğitimi alır.
- Rol bazlı güvenlik eğitimleri düzenlenir.
- Eğitim etkinliği düzenli olarak değerlendirilir.

### 11.2. Farkındalık Programı

- Düzenli güvenlik bültenleri yayınlanır.
- Sosyal mühendislik simülasyonları yapılır.
- Güvenlik ihlal örnekleri ve alınan dersler paylaşılır.
- Güvenli davranış teşvik edilir ve ödüllendirilir.

## 12. Üçüncü Taraf Güvenliği

### 12.1. Tedarikçi Yönetimi

- Tedarikçiler risk bazlı değerlendirilir.
- Tedarikçilerle veri işleme ve gizlilik sözleşmeleri yapılır.
- Tedarikçilerin güvenlik uyumluluğu düzenli olarak denetlenir.
- Tedarikçi erişimleri en az ayrıcalık prensibiyle sınırlandırılır.

### 12.2. Bulut Hizmetleri Güvenliği

- Bulut hizmet sağlayıcıları güvenlik kriterleri doğrultusunda seçilir.
- Sorumluluk paylaşım modeli açıkça tanımlanır.
- Bulut üzerinde saklanan veriler şifrelenir.
- Bulut hizmetleri izlenir ve denetlenir.

## 13. Mobil Uygulama Güvenliği

### 13.1. Mobil Uygulama Geliştirme Güvenliği

- OWASP Mobil Top 10 güvenlik riskleri ele alınır.
- Mobil uygulama güvenli kodlama standartları uygulanır.
- Yerel depolama güvenliği sağlanır.
- Kod obfuskasyonu ve anti-tamper önlemleri alınır.

### 13.2. Mobil Kimlik Doğrulama ve Yetkilendirme

- Biometrik kimlik doğrulama desteklenir.
- Mobil oturum yönetimi güvenli şekilde yapılır.
- Offline kullanım için güvenli token yönetimi uygulanır.
- Mobil cihaz kaydı ve yönetimi sağlanır.

## 14. İletişim ve İhlal Bildirimi

### 14.1. İhlal Bildirimi

- Güvenlik olayları ve ihlalleri için resmi bildirim prosedürü tanımlanmıştır.
- İhlal bildirimi için iletişim kanalları ve sorumlular belirlenmiştir.
- KVKK'ya uygun şekilde bildirim süreçleri uygulanır.
- İhlal bildirimi ve yönetimi için zaman çizelgesi belirlenmiştir.

### 14.2. İletişim Bilgileri

- Güvenlik olayları bildirim e-postası: guvenlik@kouakademik.edu.tr
- Güvenlik olayları acil telefon hattı: 0262 XXX XX XX
- KVKK sorumlusu e-postası: kvkk@kouakademik.edu.tr
- BT Güvenlik Ekibi iletişim bilgileri

## 15. Onay ve Yürürlük

Bu güvenlik politikası belgesi, Kocaeli Üniversitesi Rektörlüğü tarafından onaylanmış ve yürürlüğe konulmuştur.

| Versiyon | Tarih | Onaylayan | Açıklama |
|----------|-------|-----------|----------|
| 1.0 | DD/MM/YYYY | [Rektör İsmi] | İlk yayın |

Bu politika, yürürlük tarihinden itibaren tüm sistem kullanıcıları, yöneticileri ve geliştiricileri için bağlayıcıdır. 