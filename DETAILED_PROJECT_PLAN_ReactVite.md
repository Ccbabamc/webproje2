# KOCAELİ ÜNİVERSİTESİ AKADEMİK PERSONEL BAŞVURU SİSTEMİ - DETAYLI PROJE PLANI (React + Vite Frontend)

**Doküman Sürümü:** 1.2 (React + Vite Frontend Kararı)
**Hazırlanma Tarihi:** 2025-03-29
**Referans PRD:** akademik_personel_basvuru_sistemi_PRD_v1_20250317
**Teknoloji Kararı:** Frontend için React (Vite + TypeScript + Shadcn UI) kullanılacaktır. Mevcut Next.js yapısı temizlenecektir.

---

**İÇİNDEKİLER**

1.  [Proje Özeti](#1-proje-özeti)
2.  [Amaç ve Hedefler](#2-amaç-ve-hedefler)
3.  [Kapsam (İçerikler ve Hariç Tutulanlar)](#3-kapsam-i̇çerikler-ve-hariç-tutulanlar)
4.  [Teslim Edilecekler](#4-teslim-edilecekler)
5.  [Paydaşlar](#5-paydaşlar)
6.  [Varsayımlar](#6-varsayımlar)
7.  [Kısıtlamalar](#7-kısıtlamalar)
8.  [Yüksek Seviye Mimari Tasarım](#8-yüksek-seviye-mimari-tasarım)
9.  [İş Kırılım Yapısı (WBS) / Detaylı Özellik Listesi](#9-i̇ş-kırılım-yapısı-wbs--detaylı-özellik-listesi-epik-ve-kullanıcı-hikayesi-bazlı)
10. [Geliştirme Metodolojisi](#10-geliştirme-metodolojisi)
11. [Takım Yapısı ve Roller](#11-takım-yapısı-ve-roller)
12. [Teknoloji Yığını](#12-teknoloji-yığını-react--vite-frontend-ile-güncellenmiş)
13. [Geliştirme Ortamı ve Araçlar](#13-geliştirme-ortamı-ve-araçlar)
14. [Test Stratejisi](#14-test-stratejisi)
15. [Dağıtım (Deployment) Stratejisi](#15-dağıtım-deployment-stratejisi)
16. [Risk Yönetimi Planı](#16-risk-yönetimi-planı)
17. [İletişim Planı](#17-i̇letişim-planı)
18. [Detaylı Proje Takvimi ve Kilometre Taşları](#18-detaylı-proje-takvimi-ve-kilometre-taşları)
19. [Bütçe ve Kaynaklar (Taslak)](#19-bütçe-ve-kaynaklar-taslak)
20. [Başarı Metrikleri](#20-başarı-metrikleri)
21. [Bakım ve Destek Planı](#21-bakım-ve-destek-planı)

---

## 1. PROJE ÖZETİ

Bu proje, Kocaeli Üniversitesi (KOÜ) akademik personel (Dr. Öğr. Üyesi, Doçent, Profesör) alım süreçlerini modernize etmeyi amaçlamaktadır. Mevcut manuel veya yarı dijital süreçlerin yerine, başvurudan değerlendirmeye kadar tüm aşamaları kapsayan, şeffaf, verimli ve kullanıcı dostu, web tabanlı bir "Akademik Personel Başvuru Sistemi" geliştirilecektir. Sistem, adaylar, ilanları yöneten adminler, kriterleri belirleyen ve süreci yöneten yöneticiler ile başvuruları değerlendiren jüri üyeleri olmak üzere dört ana kullanıcı rolüne hizmet edecektir. KOÜ Atama Yönergesi'ne tam uyumluluk ve e-Devlet gibi ulusal sistemlerle entegrasyon hedeflenmektedir.

## 2. AMAÇ VE HEDEFLER

*   **Ana Amaç:** KOÜ akademik personel başvuru ve değerlendirme süreçlerini dijitalleştirmek, standartlaştırmak ve optimize etmek.
*   **SMART Hedefler:**
    *   Başvuru ve ön değerlendirme süreçlerindeki manuel iş yükünü ilk 6 ay içinde en az %50 azaltmak.
    *   Adayların başvuru durumlarını anlık ve şeffaf bir şekilde takip edebilmelerini sağlamak (%100 kapsama).
    *   KOÜ Atama Yönergesi'ndeki kriterlere göre puanlamayı otomatikleştirerek değerlendirme tutarlılığını artırmak ve süresini %30 kısaltmak.
    *   Sistemin canlıya geçişinden sonraki ilk 12 ay içinde %99.9 çalışma süresi (uptime) sağlamak.
    *   Kullanıcı (Aday, Yönetici, Jüri) memnuniyetini ilk 3 ay sonunda yapılacak anketlerde 5 üzerinden en az 4.0 seviyesine çıkarmak.

## 3. KAPSAM (İÇERİKLER VE HARİÇ TUTULANLAR)

*   **İçerikler:**
    *   Rol Bazlı Kullanıcı Yönetimi (Aday, Admin, Yönetici, Jüri) ve Kimlik Doğrulama (Şifre, e-Devlet).
    *   İlan Yönetimi (Oluşturma, Düzenleme, Yayınlama, Arşivleme).
    *   Aday Başvuru Süreci (İlan Görüntüleme, Başvuru Formu Doldurma, Belge Yükleme - Yayın, Atıf, Kanıt vb.).
    *   Başvuru Takibi (Adaylar için durum görüntüleme).
    *   Modüler Kadro Kriter Yönetimi (Fakülte/Bölüm/Kadro bazlı, puanlama kuralları).
    *   Otomatik Puan Hesaplama ve Tablo 5 Oluşturma.
    *   Jüri Atama Süreci.
    *   Jüri Değerlendirme Süreci (Belge İnceleme, Rapor Yükleme, Karar Verme).
    *   Yönetici Değerlendirme ve Karar Süreci.
    *   Bildirim Sistemi (E-posta, Sistem İçi).
    *   Temel Raporlama (Başvuru istatistikleri).
    *   API Entegrasyonları (e-Devlet Kimlik Doğrulama, Nüfus Veri Doğrulama - Müsaitlik durumuna göre).
    *   Güvenlik Önlemleri (PRD'de belirtilenler).
    *   Responsive Tasarım (Mobil uyumluluk).
*   **Hariç Tutulanlar (İlk Faz İçin):**
    *   Ayrı bir mobil uygulama (Web arayüzü responsive olacak).
    *   KOÜ Öğrenci Bilgi Sistemi (ÖBS) veya Personel Bilgi Sistemi (PBS) ile doğrudan veri entegrasyonu (Gelecek fazlarda değerlendirilebilir).
    *   Çevrimdışı çalışma modu.
    *   Gelişmiş analitik ve öngörüsel raporlama modülleri.
    *   SMS ile bildirim (Opsiyonel olarak belirtilmiş, ilk fazda e-posta ve sistem içi yeterli).
    *   A1-A5 dışındaki spesifik ve nadir yayın kategorileri için özel modüller (Genel bir "Diğer" kategorisi olabilir).

## 4. TESLİM EDİLECEKLER

1.  Canlıya Alınmış Web Uygulaması (Frontend - React+Vite ve Backend - Django).
2.  Kurulumu Yapılmış Veritabanı ve Şeması.
3.  API Entegrasyon Dokümantasyonu (varsa).
4.  Teknik Sistem Mimarisi Dokümantasyonu.
5.  Kullanıcı Kılavuzları (Her rol için ayrı).
6.  Test Senaryoları, Planları ve Sonuç Raporları (Unit, Integration, E2E, UAT, Performans, Güvenlik).
7.  Kaynak Kodları ve Versiyon Kontrol Sistemi Erişimi.
8.  Deployment (Dağıtım) Scriptleri ve Talimatları.
9.  Acil Durum Geri Yükleme Planı.

## 5. PAYDAŞLAR

*   **Proje Sponsoru:** KOÜ Rektörlüğü / İlgili Rektör Yardımcılığı.
*   **Proje Yöneticisi (KOÜ Tarafı):** Belirlenecek (Örn: Personel Daire Başkanlığı Yetkilisi).
*   **Son Kullanıcılar:** Akademik Personel Adayları, Jüri Üyeleri.
*   **Sistem Yöneticileri:** KOÜ Personel Daire Başkanlığı Admin Kullanıcıları, Sistemi yönetecek Yöneticiler (Birim Yöneticileri?).
*   **Teknik Paydaşlar:** KOÜ Bilgi İşlem Daire Başkanlığı (Altyapı, Güvenlik, Entegrasyon Desteği).
*   **Geliştirme Ekibi:** Proje Yöneticisi (Yazılım), Yazılım Geliştiriciler (Frontend - React, Backend - Django), QA Mühendisi, UI/UX Tasarımcısı, DevOps Mühendisi (gerekiyorsa).

## 6. VARSAYIMLAR

*   PRD'de belirtilen "Açık Sorular" geliştirme fazları öncesinde KOÜ tarafından netleştirilecektir.
*   KOÜ Atama Yönergesi'nin güncel ve nihai hali proje ekibine sunulacaktır.
*   e-Devlet ve Nüfus Müdürlüğü API'lerine erişim için gerekli izinler ve teknik destek KOÜ tarafından sağlanacaktır (Test ve canlı ortamlar için).
*   KOÜ Bilgi İşlem Daire Başkanlığı, sunucu altyapısı, ağ yapılandırması ve güvenlik duvarı ayarları konusunda destek verecektir.
*   Belirlenen paydaşlar (Admin, Yönetici, Jüri temsilcileri) geri bildirim, test (UAT) ve onay süreçleri için makul sürelerde erişilebilir olacaktır.
*   Sistem için gerekli kurumsal içerikler (logo, resmi metinler, başlangıç kriter setleri vb.) KOÜ tarafından zamanında sağlanacaktır.
*   Proje için gerekli bütçe ve kaynaklar (insan gücü, lisanslar, altyapı) proje süresince devamlılık gösterecektir.

## 7. KISITLAMALAR

*   **Zaman:** Proje takvimine uyulması kritiktir (Bkz. Bölüm 18). Toplam süre yaklaşık 26 hafta olarak öngörülmektedir.
*   **Bütçe:** Belirlenecek proje bütçesi aşılmamalıdır (Bkz. Bölüm 19).
*   **Teknoloji:** Frontend için React (Vite, TypeScript, Shadcn UI), Backend için Django (Python), Veritabanı için PostgreSQL kullanılacaktır.
*   **Mevzuat:** Sistem, KVKK (Kişisel Verilerin Korunması Kanunu) ve KOÜ'nün ilgili yönetmeliklerine tam uyumlu olmalıdır.
*   **Kaynaklar:** Proje ekibinin belirlenen büyüklüğü ve yetkinlikleri dahilinde çalışılacaktır.
*   **Entegrasyon Bağımlılıkları:** Dış API'ların (e-Devlet, Nüfus) performansı ve erişilebilirliği proje hızını etkileyebilir.

## 8. YÜKSEK SEVİYE MİMARİ TASARIM

*   **Model:** Üç Katmanlı Mimari (Sunum, İş Mantığı, Veri Erişimi).
*   **Sunum Katmanı (Frontend):**
    *   Teknoloji: React (v18+, Vite ile SPA - Single Page Application), TypeScript
    *   Sorumluluklar: Kullanıcı arayüzü oluşturma (Shadcn UI/Tailwind CSS ile), kullanıcı girdilerini alma, Backend API ile iletişim (Axios), durum yönetimi (Zustand/Redux Toolkit/Context API), yönlendirme (React Router).
*   **İş Mantığı Katmanı (Backend):**
    *   Teknoloji: Django / Django REST Framework (Python)
    *   Sorumluluklar: API endpoint'leri sağlama, iş kurallarını uygulama (puanlama, kriter kontrolü vb.), kimlik doğrulama ve yetkilendirme (JWT), veri doğrulama, dış API'lerle entegrasyon, veritabanı işlemleri için Veri Erişim Katmanı ile iletişim.
*   **Veri Erişim Katmanı:**
    *   Teknoloji: PostgreSQL Veritabanı, Django ORM
    *   Sorumluluklar: Verilerin kalıcı olarak saklanması, veri bütünlüğünün sağlanması, sorgu optimizasyonu.
*   **Diğer Bileşenler:**
    *   **Dosya Depolama:** AWS S3 veya Firebase Storage (Karar verilecek - Ölçeklenebilirlik ve maliyet etkinliği öncelikli).
    *   **Bildirim Servisi:** Firebase Cloud Messaging (FCM) (Sistem içi ve potansiyel push bildirimler için) / E-posta için Django'nun mail modülü veya harici servis (SendGrid/Mailgun).
    *   **PDF Üretimi:** `reportlab` veya `WeasyPrint` gibi Python kütüphaneleri.
    *   **Sunucu Altyapısı:** KOÜ sunucuları veya Bulut (AWS/Azure/GCP - Karar verilecek). Docker ile konteynerleştirme tavsiye edilir.
    *   **Web Sunucusu/Proxy:** Nginx veya Apache.
    *   **CI/CD:** GitLab CI, Jenkins veya GitHub Actions.

```mermaid
graph TD
    subgraph Kullanıcı Arayüzü (Browser)
        Frontend[React SPA (Vite, TypeScript, Shadcn UI)]
    end

    subgraph Sunucu Altyapısı (KOÜ / Bulut)
        Proxy[Nginx / Apache]
        Backend[Django REST API (Python)]
        Database[(PostgreSQL)]
        FileStorage[(AWS S3 / Firebase Storage)]
        Notification[Bildirim Servisi (E-posta / FCM)]
    end

    subgraph Dış Servisler
        eDevlet[e-Devlet API]
        Nufus[Nüfus API (Opsiyonel)]
    end

    Frontend -- API İstekleri (HTTPS) --> Proxy
    Proxy -- İstek Yönlendirme --> Backend
    Backend -- Veritabanı İşlemleri --> Database
    Backend -- Dosya İşlemleri --> FileStorage
    Backend -- Bildirim Gönderme --> Notification
    Backend -- API Çağrıları --> eDevlet
    Backend -- API Çağrıları --> Nufus
```

## 9. İŞ KIRILIM YAPISI (WBS) / DETAYLI ÖZELLİK LİSTESİ (EPİK VE KULLANICI HİKAYESİ BAZLI)

**(PRD'deki F#.# kodları ile ilişkilendirilmiştir. Frontend görevleri React'e göre uyarlanmıştır.)**

*   **Epik 1: Proje Kurulumu ve Temel Yapı**
    *   Görev 1.1: Geliştirme ortamlarının kurulması (Yerel, Staging, Prod).
    *   Görev 1.2: Versiyon kontrol sistemi (Git) ve repo kurulumu.
    *   Görev 1.3: CI/CD pipeline temel kurulumu.
    *   Görev 1.4: Temel Frontend (React + Vite + TypeScript) projesi yapılandırma (**Mevcut Next.js yapısı temizlenecek**, gerekli eklemeler yapılacak: Router, State Management).
    *   Görev 1.5: Temel Backend (Django) projesi oluşturma ve yapılandırma.
    *   Görev 1.6: Veritabanı (PostgreSQL) kurulumu ve bağlantı yapılandırması.
    *   Görev 1.7: Temel UI Kiti (Shadcn UI/Tailwind) ve Stil Rehberi entegrasyonu (D1.1, D1.5).
*   **Epik 2: Kullanıcı Yönetimi ve Kimlik Doğrulama**
    *   Hikaye 2.1 (F1.1): 4 Farklı kullanıcı rolünün (Aday, Admin, Yönetici, Jüri) model ve yetki tanımlamaları (Backend).
    *   Hikaye 2.2 (F1.2, F1.4): TC Kimlik No ve Şifre ile Güvenli Giriş Sistemi (React Formları, API Bağlantısı).
    *   Hikaye 2.3 (F1.3, T1.7): e-Devlet ile Kimlik Doğrulama Entegrasyonu (Backend API çağrısı, React yönlendirme/callback yönetimi).
    *   Hikaye 2.4 (F1.5): Şifre Sıfırlama Mekanizması (E-posta ile Backend, React Formları).
    *   Hikaye 2.5 (F1.6): Yönetici tarafından Jüri Üyesi Kayıt Ekranı/İşlevi (React Arayüzü, API Bağlantısı).
    *   Hikaye 2.6 (T1.4): JWT tabanlı oturum yönetimi implementasyonu (Backend ve React tarafında token saklama/kullanma).
*   **Epik 3: İlan Yönetimi (Admin Rolü)**
    *   Hikaye 3.1 (F2.1, F2.6): Yeni İlan Ekleme Formu ve İşlevi (React Formları, API Bağlantısı).
    *   Hikaye 3.2 (F2.2): İlan Kategorileri (Dr.Öğr.Üy, Doç, Prof) veri modeli (Backend) ve filtreleme (React Arayüzü).
    *   Hikaye 3.3 (F2.3): İlan Başlangıç/Bitiş Tarihi belirleme ve kontrolü (React Date Picker, Backend validasyon).
    *   Hikaye 3.4 (F2.4): İlan için gerekli belge listesi tanımlama alanı (React Arayüzü).
    *   Hikaye 3.5 (F2.5): Mevcut İlanları Düzenleme İşlevi (React Formları, API Bağlantısı).
    *   Hikaye 3.6 (F2.7): İlan Durumu (Aktif/Pasif) Yönetimi (React Arayüzü, API Bağlantısı).
    *   Hikaye 3.7 (F2.8): İlan Listeleme ve Filtreleme Ekranı (Admin) (React Arayüzü).
    *   Hikaye 3.8 (F3.1): Adaylar için Ana Sayfada Aktif İlanları Listeleme (React Arayüzü).
*   **Epik 4: Başvuru Süreci (Aday Rolü)**
    *   Hikaye 4.1 (F3.2): İlan Detay Sayfası Görüntüleme (React Arayüzü).
    *   Hikaye 4.2 (F3.3, F3.5, F3.6, F3.7, F3.9): Başvuru Formu (Adımlar: Kişisel Bilgiler, Eğitim, Akademik Çalışmalar, Belgeler - Yayın, Atıf, Konferans, Başlıca Yazar vb.) (React Çok Adımlı Form, API Bağlantısı).
    *   Hikaye 4.3 (T1.5): Belge Yükleme Altyapısı (React upload bileşeni, Backend storage entegrasyonu).
    *   Hikaye 4.4 (F3.8): Başvuru sırasında eksik belge/alan kontrolü ve validasyon (React Hook Form/Zod, Backend validasyon).
    *   Hikaye 4.5 (F3.10): Başvuru Önizleme İşlevi (React Arayüzü).
    *   Hikaye 4.6: Başvuruyu Tamamlama ve Sisteme Kaydetme İşlevi (API Bağlantısı).
    *   Hikaye 4.7 (F3.4): Aday için "Başvurularım" ve Durum Takip Sayfası (React Arayüzü).
*   **Epik 5: Kriter Yönetimi ve Otomatik Puanlama (Yönetici Rolü)**
    *   Hikaye 5.1 (F4.1, F4.2, F6.1, F6.2, F6.3, F6.6): Modüler Kriter Yönetim Paneli (Fakülte/Kadro bazlı, min. puan/makale, A1-A5 vb. kurallar) (React Arayüzü, API Bağlantısı).
    *   Hikaye 5.2 (F6.4): Kriterlerde "Başlıca Yazar" durumu için puanlama kuralı tanımlama (React Arayüzü).
    *   Hikaye 5.3 (F4.3): Adayın yüklediği verilere ve tanımlı kriterlere göre Otomatik Puan Hesaplama Motoru (Backend).
    *   Hikaye 5.4 (F4.4, F7.4, T1.8): Hesaplanan puanlar ve aday verileri ile Tablo 5'in Otomatik Oluşturulması ve PDF İndirme İşlevi (Backend PDF üretimi, React indirme butonu).
*   **Epik 6: Değerlendirme Süreci (Yönetici ve Jüri Rolleri)**
    *   Hikaye 6.1 (F4.5): Yönetici için Başvuru Süresi Biten İlanların Başvuru Listesi ve Sayısı Görüntüleme (React Arayüzü).
    *   Hikaye 6.2 (F4.6): Yönetici için Jüri Atama Ekranı (Başvuru seçimi, Jüri seçimi) (React Arayüzü).
    *   Hikaye 6.3 (F5.1): Jüri Üyesi için Atanan Başvuruları Listeleme Ekranı (React Arayüzü).
    *   Hikaye 6.4 (F5.1): Jüri Üyesi için Aday Başvuru Detayları ve Belgelerini İnceleme Arayüzü (React Arayüzü).
    *   Hikaye 6.5 (F5.2, F5.3): Jüri Üyesi Değerlendirme Formu (Zorunlu alanlar) ve Rapor Yükleme İşlevi (React Formları, Belge Yükleme).
    *   Hikaye 6.6 (F5.4): Jüri Üyesi Nihai Karar (Olumlu/Olumsuz) Girişi (React Arayüzü).
    *   Hikaye 6.7 (F5.6): Jüri üyelerinin birbirlerinin kararlarını görememesi yetkilendirmesi (Backend).
    *   Hikaye 6.8 (F4.7): Yönetici için Jüri Değerlendirme Raporlarını Görüntüleme Ekranı (React Arayüzü).
    *   Hikaye 6.9 (F4.8): Yönetici için Nihai Karar Verme Arayüzü (Jüri raporları ışığında) (React Arayüzü).
*   **Epik 7: Bildirim ve Raporlama**
    *   Hikaye 7.1 (F7.1, T1.6): Adaylara Başvuru Durumu Değişikliklerinde Otomatik E-posta Bildirimi (Backend).
    *   Hikaye 7.2 (F7.2): Sistem İçi Bildirim Mekanizması (Tüm roller için ilgili olaylarda) (Backend, React Bildirim Bileşeni).
    *   Hikaye 7.3 (F7.3): Başvuru Belgelerinin Toplu PDF olarak indirilebilmesi (Yönetici/Jüri için) (Backend PDF birleştirme, React indirme).
    *   Hikaye 7.4 (F7.5): Yöneticiler için Temel Başvuru İstatistikleri Raporlama Ekranı (React Arayüzü, belki Recharts gibi bir kütüphane).
    *   Hikaye 7.5 (F7.6): Jüri Değerlendirme Raporlarının Sistem Üzerinden İndirilebilmesi (Yönetici) (React indirme).
    *   Hikaye 7.6 (F4.9): Yönetici tarafından Aday Sonuç Bildirimi Tetikleme (E-posta/Sistem içi) (React Buton, Backend İşlemi).
*   **Epik 8: Güvenlik ve Performans**
    *   Hikaye 8.1 (G7.1, G7.2): PRD'de belirtilen güvenlik önlemlerinin (Rol bazlı yetkilendirme, şifreleme, XSS/CSRF koruma, SQLi önleme, HTTPS) implementasyonu (Backend ve Frontend).
    *   Hikaye 8.2 (G7.3): Kritik işlemlerin loglanması mekanizması (Backend).
    *   Hikaye 8.3 (T1.9, T1.10): Performans Optimizasyonları (Veritabanı sorguları, API yanıt süreleri, React bileşen optimizasyonu, kod bölme).
    *   Hikaye 8.4 (T1.12): Düzenli Veritabanı Yedekleme Stratejisi ve Uygulaması (DevOps/Altyapı).
*   **Epik 9: Test ve Dağıtım**
    *   Görev 9.1: Test planlarının hazırlanması (Unit, Int, E2E, UAT, Perf, Sec).
    *   Görev 9.2: Unit ve Integration testlerin yazılması (Backend: Pytest, Frontend: Jest/React Testing Library).
    *   Görev 9.3: E2E test senaryolarının otomatikleştirilmesi (Cypress vb.).
    *   Görev 9.4: Staging ortamının hazırlanması.
    *   Görev 9.5: Kullanıcı Kabul Testlerinin (UAT) organize edilmesi ve yürütülmesi.
    *   Görev 9.6: Performans ve Güvenlik testlerinin yapılması.
    *   Görev 9.7: Prod ortamının hazırlanması ve deployment scriptlerinin oluşturulması.
    *   Görev 9.8: Canlıya geçiş (Deployment).
    *   Görev 9.9: Canlıya geçiş sonrası izleme ve acil durum müdahale planı.

## 10. GELİŞTİRME METODOLOJİSİ

*   **Metodoloji:** Agile (Scrum)
*   **Sprint Süresi:** 2 Hafta
*   **Seremoniler:**
    *   Sprint Planlama (Her sprint başında)
    *   Günlük Scrum (Her gün 15 dk)
    *   Sprint Değerlendirme (Her sprint sonunda, paydaş katılımıyla demo)
    *   Sprint Retrospektifi (Her sprint sonunda, ekip içi iyileştirme)
*   **Araçlar:** Jira, Trello veya benzeri bir proje yönetim/takip aracı.

## 11. TAKIM YAPISI VE ROLLER

*   **Proje Yöneticisi (Yazılım):** Planlama, takip, koordinasyon, risk yönetimi, iletişim.
*   **UI/UX Tasarımcısı:** Arayüz tasarımı, kullanıcı deneyimi akışları, prototipleme (Projenin başında ve ihtiyaç oldukça).
*   **Frontend Geliştirici(ler) (1-2 Kişi):** React (TypeScript, Shadcn UI) ile arayüz geliştirme.
*   **Backend Geliştirici(ler) (1-2 Kişi):** Django ile API ve iş mantığı geliştirme.
*   **QA Mühendisi:** Test planlama, manuel ve otomatik testler, hata takibi.
*   **DevOps Mühendisi (Opsiyonel/Part-time):** Altyapı, CI/CD, deployment süreçleri.

## 12. TEKNOLOJİ YIĞINI (REACT + VITE FRONTEND İLE GÜNCELLENMİŞ)

*   **Frontend:** React (v18+), TypeScript, Vite, State Management (Zustand/Redux Toolkit/Context API - **Seçilecek**), React Router, Axios, Shadcn UI (Tailwind CSS üzerine kurulu), Form Yönetimi (React Hook Form), Şema Validasyonu (Zod).
*   **Backend:** Python (v3.9+), Django (v4+), Django REST Framework
*   **Veritabanı:** PostgreSQL (v14+)
*   **Kimlik Doğrulama:** JWT (djangorestframework-simplejwt)
*   **Dosya Depolama:** AWS S3 veya Firebase Cloud Storage (**Seçilecek**)
*   **API Entegrasyon:** `requests` kütüphanesi (Python)
*   **PDF Üretimi:** `reportlab` veya `WeasyPrint` (Python - **Seçilecek**)
*   **Bildirim:** Django email backend, FCM (pyfcm veya drf-firebase-auth - **Seçilecek**)
*   **Test:**
    *   Backend: Pytest, Coverage.py
    *   Frontend: Jest, React Testing Library (Unit/Integration), Cypress (E2E)
*   **Konteynerleştirme:** Docker, Docker Compose
*   **Web Sunucusu/Proxy:** Nginx

## 13. GELİŞTİRME ORTAMI VE ARAÇLAR

*   **Versiyon Kontrol:** Git (Platform: GitLab / GitHub / Bitbucket - KOÜ tercihine göre)
*   **Branching Stratejisi:** Gitflow (veya benzeri: main, develop, feature/*, release/*, hotfix/*)
*   **IDE:** VS Code, PyCharm
*   **İletişim:** Slack / Microsoft Teams
*   **Proje Yönetimi:** Jira / Trello
*   **CI/CD:** GitLab CI / Jenkins / GitHub Actions
*   **Yerel Ortam:** Docker Compose ile tüm servislerin (web, db, vb.) kolayca ayağa kaldırılması.
*   **Paket Yöneticisi:** pnpm (Frontend - mevcut yapıya göre), pip (Backend)

## 14. TEST STRATEJİSİ

*   **Birim Testleri (Unit Tests):** Geliştiriciler tarafından yazılır. Backend (fonksiyonlar, sınıflar, modeller - Pytest), Frontend (bileşenler, hook'lar, state yönetimi - Jest/React Testing Library). Hedef kod kapsamı: %70+.
*   **Entegrasyon Testleri:** API endpoint'lerinin veritabanı ve diğer servislerle doğru çalıştığını test eder (Pytest ile Django test client). API-Dış Servis etkileşimleri için mock servisler kullanılabilir. Frontend'de bileşenlerin API çağrıları ile entegrasyonu test edilebilir (React Testing Library ile mock API).
*   **Uçtan Uca Testler (E2E):** Kritik kullanıcı akışları (Başvuru yapma, İlan ekleme, Değerlendirme yapma vb.) tarayıcı üzerinde otomatikleştirilir (Cypress).
*   **Kullanıcı Kabul Testleri (UAT):** Paydaşlar (Admin, Yönetici, Jüri temsilcileri) tarafından Staging ortamında, gerçek senaryolar üzerinden yapılır. Geri bildirimler toplanır ve hatalar düzeltilir.
*   **Güvenlik Testleri:** OWASP Top 10 zafiyet taramaları, yetkilendirme kontrolleri, veri sızıntısı kontrolleri. Mümkünse dışarıdan penetrasyon testi.
*   **Performans Testleri:** Staging ortamında yük testleri (JMeter, k6) ile T1.9 ve T1.10 gereksinimlerinin karşılandığı doğrulanır. Veritabanı sorgu optimizasyonu, API ve React performans iyileştirmeleri yapılır.
*   **Regresyon Testleri:** Her yeni sürüm öncesinde, yapılan değişikliklerin mevcut işlevselliği bozmadığından emin olmak için ilgili testler (otomatik ve manuel) tekrar çalıştırılır.

## 15. DAĞITIM (DEPLOYMENT) STRATEJİSİ

1.  **Ortamlar:** Development (Yerel), Testing (CI/CD ile otomatik), Staging (UAT ve Demo için), Production (Canlı).
2.  **Staging:** UAT ve son kontroller için Prod ortamının bir kopyası niteliğinde.
3.  **Production:** CI/CD pipeline ile otomatik veya yarı otomatik deployment.
    *   **Yöntem:** Mavi/Yeşil (Blue/Green) deployment veya Canary Release stratejisi (sıfır kesinti veya minimum kesinti hedeflenir).
    *   **Veritabanı Geçişleri:** Django Migrations kullanılır ve dikkatlice yönetilir.
    *   **Geri Alma Planı (Rollback):** Deployment başarısız olursa veya kritik sorunlar çıkarsa, önceki stabil sürüme hızlıca geri dönebilmek için plan ve scriptler hazır olmalıdır.
4.  **Sıklık:** Sprint sonlarında Staging'e, UAT onayı sonrası Prod'a deployment yapılması hedeflenir.

## 16. RİSK YÖNETİMİ PLANI

| Risk ID | Risk Açıklaması                                      | Olasılık (1-5) | Etki (1-5) | Öncelik | Önleyici / Azaltıcı Aksiyonlar                                                                 | Sorumlu Kişi     |
| :------ | :--------------------------------------------------- | :------------- | :--------- | :------ | :--------------------------------------------------------------------------------------------- | :--------------- |
| R01     | KOÜ Atama Yönergesi/Puanlama Kurallarında Belirsizlik | 3              | 5          | Yüksek  | Açık soruların erken netleştirilmesi, Yönetici rolü ile sık prototip ve demo seansları.      | Proje Yöneticisi |
| R02     | e-Devlet/Nüfus API Entegrasyonunda Gecikme/Sorun     | 3              | 4          | Yüksek  | Başvuru sürecini erken başlatma, Mock API'ler geliştirme, KOÜ IT ile yakın koordinasyon.       | Backend Lead     |
| R03     | Paydaşların Geri Bildirim/UAT İçin Müsait Olmaması    | 3              | 3          | Orta    | İletişim Planı'nda belirtilen düzenli toplantılar, net geri bildirim süreleri tanımlama.        | Proje Yöneticisi |
| R04     | Kapsam Kayması (Scope Creep)                         | 4              | 4          | Yüksek  | Değişiklik Yönetim Süreci oluşturma, Tüm değişiklik taleplerini etki/öncelik analizine tabi tutma. | Proje Yöneticisi |
| R05     | Teknik Zorluklar (Performans, Belge Yönetimi vb.)   | 2              | 4          | Orta    | Riskli alanlar için Proof-of-Concept (PoC) çalışmaları, Erken performans testleri.              | Teknik Lead      |
| R06     | Güvenlik Açıkları                                    | 2              | 5          | Yüksek  | Güvenli kodlama pratikleri, Kapsamlı güvenlik testleri (iç/dış), Bağımlılıkları güncel tutma. | QA / Dev Team    |
| R07     | Ekip İçi Bilgi Eksikliği / Yetkinlik Sorunları       | 2              | 3          | Düşük   | Eğitimler, Pair Programming, Kod incelemeleri (Code Review).                                    | Proje Yöneticisi |

## 17. İLETİŞİM PLANI

*   **Günlük Stand-up:** (15 dk) Ekip içi ilerleme, engeller.
*   **Haftalık Ekip Toplantısı:** (1 Saat) Genel durum, riskler, planlama.
*   **Sprint Değerlendirme (Demo):** (1-2 Saat) Sprint sonunda paydaşlara yapılan işlerin sunumu, geri bildirim alma.
*   **Sprint Retrospektifi:** (1 Saat) Sprint sonunda ekip içi değerlendirme.
*   **Paydaş Toplantıları:** İhtiyaç bazlı veya düzenli (Örn: 2 haftada bir KOÜ Proje Yöneticisi ile).
*   **Raporlama:** Haftalık İlerleme Raporu (Proje Yöneticisi tarafından paydaşlara).
*   **Araçlar:** E-posta, Slack/Teams, Jira/Trello.
*   **Acil Durum İletişimi:** Belirlenmiş telefon numaraları / iletişim kanalları.

## 18. DETAYLI PROJE TAKVİMİ VE KİLOMETRE TAŞLARI

**(Yüksek seviye Gantt şeması aşağıdadır. Detaylı görevler proje yönetim aracında takip edilmelidir.)**

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title KOU Akademik Başvuru Sistemi Proje Takvimi (Tahmini - React+Vite)
    excludes    weekends
    %% `axisFormat` defaults to `%Y-%m-%d`

    section Faz 0: Hazırlık ve Planlama (3 Hafta)
    Detaylı Analiz & Onaylar :a1, 2025-04-01, 14d
    Ortam Kurulumu & Oryantasyon :a2, after a1, 7d
    KM1: Plan Onaylandı : milestone, m1, 2025-04-21, 0d

    section Faz 1: Temel Yapı & Kullanıcı Yönetimi (6 Hafta)
    %% Not: Bu fazın başında Next.js temizliği ve Vite kurulumu yapılacak.
    Next.js Temizliği & Vite Kurulumu :a2b, after a2, 3d
    Epik 1 & 2 Geliştirme (Sprint 1-2) :a3, after a2b, 25d
    Test & Geri Bildirim (Sprint 3) :a4, after a3, 14d
    KM2: Kullanıcı Yönetimi Tamamlandı : milestone, m2, 2025-06-05, 0d

    section Faz 2: İlan & Başvuru Süreci (6 Hafta)
    Epik 3 & 4 Geliştirme (Sprint 4-5) :a5, after a4, 28d
    Test & Entegrasyon (Sprint 6) :a6, after a5, 14d
    KM3: Başvuru & İlan Yönetimi Tamamlandı : milestone, m3, 2025-07-17, 0d

    section Faz 3: Kriter, Puanlama & Değerlendirme (4 Hafta)
    Epik 5 Geliştirme (Sprint 7) :a7, after a6, 14d
    Epik 6 Geliştirme (Sprint 8) :a8, after a7, 14d
    KM4: Değerlendirme Modülleri Tamamlandı : milestone, m4, 2025-08-14, 0d

    section Faz 4: Bildirim, Raporlama & Tamamlama (4 Hafta)
    Epik 7 & 8 Geliştirme (Sprint 9) :a9, after a8, 14d
    Entegrasyon Test & Hata Düzeltme (Sprint 10) :a10, after a9, 14d
    KM5: Fonksiyonel Geliştirmeler Tamamlandı : milestone, m5, 2025-09-11, 0d

    section Faz 5: Test ve Kabul (4 Hafta)
    Yoğun QA Testleri :a11, after a10, 14d
    UAT & Son Düzeltmeler :a12, after a11, 14d
    KM6: UAT Onaylandı : milestone, m6, 2025-10-09, 0d

    section Faz 6: Canlıya Geçiş ve İzleme (1 Hafta + Sürekli)
    Canlı Ortam Hazırlığı & Deployment :a13, after a12, 7d
    Hypercare & İzleme :a14, after a13, 14d
    KM7: Sistem Canlıda : milestone, m7, 2025-10-20, 0d
```

## 19. BÜTÇE VE KAYNAKLAR (TASLAK)

*   **İnsan Kaynakları:** Proje Yöneticisi, Tasarımcı, Geliştiriciler (Frontend/Backend), QA Mühendisi (Tahmini Adam/Gün veya Adam/Ay maliyeti hesaplanmalı).
*   **Yazılım Lisansları:** Gerekliyse (Örn: Proje Yönetim Aracı, Özel Kütüphaneler). Çoğunlukla açık kaynak kullanılacak.
*   **Altyapı Maliyetleri:** Sunucu (KOÜ içi veya Bulut - AWS/Azure/GCP), Veritabanı, Dosya Depolama (S3/Firebase), Alan adı, SSL Sertifikası.
*   **Dış Servis Maliyetleri:** E-posta gönderim servisi (SendGrid/Mailgun - Kullanım miktarına göre), SMS (Eğer dahil edilirse).
*   **Diğer:** Eğitim, Danışmanlık (gerekiyorsa).

**(Detaylı bütçe, kaynak planlaması ve KOÜ onayına göre ayrıca hazırlanmalıdır.)**

## 20. BAŞARI METRİKLERİ

*   **Proje Teslimatı:** Zamanında ve bütçe dahilinde tamamlanma.
*   **Fonksiyonellik:** PRD'de tanımlanan P0 ve P1 öncelikli tüm gereksinimlerin karşılanması.
*   **Performans:** Sayfa yüklenme süresi (< 3 sn), Eşzamanlı kullanıcı desteği (min 1000), Uptime (%99.9).
*   **Verimlilik Artışı:** Başvuru işleme süresindeki azalma (Hedef: %30), Manuel işlem sayısındaki azalma.
*   **Kullanıcı Memnuniyeti:** Aday, Admin, Yönetici, Jüri anketleri (Hedef: 4.0/5.0+).
*   **Hata Oranı:** Canlıya geçiş sonrası ilk 3 ayda kritik/yüksek öncelikli hata sayısının düşük olması.
*   **Benimseme Oranı:** Sistemin ilgili birimler ve adaylar tarafından aktif kullanımı.

## 21. BAKIM VE DESTEK PLANI

*   **Garanti Süresi:** Canlıya geçiş sonrası 3 ay boyunca ücretsiz hata düzeltme (Proje kapsamında oluşan hatalar için).
*   **Bakım Anlaşması (Opsiyonel):** Garanti sonrası için:
    *   Periyodik Bakım: Sistem güncellemeleri (OS, Kütüphaneler, Güvenlik Yamaları).
    *   Hata Düzeltme: Yeni oluşan hataların giderilmesi (SLA tanımlanmalı - Önceliğe göre müdahale ve çözüm süresi).
    *   Destek: Kullanıcı soruları ve küçük çaplı iyileştirme talepleri için destek.
    *   İzleme: Sistem sağlığının (performans, uptime, loglar) sürekli izlenmesi.
*   **Sorumluluk:** KOÜ Bilgi İşlem veya Geliştirici Ekip ile yapılacak anlaşmaya göre belirlenir.

---

**SONUÇ:**

Bu detaylı proje planı, Kocaeli Üniversitesi Akademik Personel Başvuru Sistemi'nin (React + Vite frontend ile) başarılı bir şekilde geliştirilmesi ve hayata geçirilmesi için bir yol haritası sunmaktadır. Planda belirtilen adımların, rollerin, süreçlerin ve takvimin takip edilmesi, projenin hedeflerine ulaşmasında kritik rol oynayacaktır. Projenin tüm aşamalarında paydaşlarla yakın iletişim ve iş birliği esastır.