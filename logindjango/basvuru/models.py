from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from ilan.models import Ilan, Kriter

User = get_user_model()

class YayinKategori(models.TextChoices):
    A1 = 'A1', _('A1')
    A2 = 'A2', _('A2')
    A3 = 'A3', _('A3')
    A4 = 'A4', _('A4')
    A5 = 'A5', _('A5')

class Basvuru(models.Model):
    class Status(models.TextChoices):
        TASLAK = 'TASLAK', _('Taslak')
        GONDERILDI = 'GONDERILDI', _('Gönderildi')
        DEGERLENDIRILDI = 'DEGERLENDIRILDI', _('Değerlendirildi')
        KABUL_EDILDI = 'KABUL_EDILDI', _('Kabul Edildi')
        RED_EDILDI = 'RED_EDILDI', _('Red Edildi')

    ilan = models.ForeignKey(Ilan, on_delete=models.CASCADE, related_name='basvurular', verbose_name=_('İlan'))
    aday = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basvurular', verbose_name=_('Aday'))
    submission_date = models.DateTimeField(_('Başvuru Tarihi'), auto_now_add=True)
    status = models.CharField(_('Durum'), max_length=20, choices=Status.choices, default=Status.TASLAK)
    tablo5_file = models.FileField(_('Tablo 5 Dosyası'), upload_to='tablo5/', null=True, blank=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Başvuru')
        verbose_name_plural = _('Başvurular')
        ordering = ['-submission_date']
        unique_together = ['ilan', 'aday']

    def __str__(self):
        return f"{self.aday.get_full_name()} - {self.ilan.baslik}"

class Belge(models.Model):
    class Type(models.TextChoices):
        YAYIN = 'YAYIN', _('Yayın')
        PROJE = 'PROJE', _('Proje')
        PATENT = 'PATENT', _('Patent')
        DIGER = 'DIGER', _('Diğer')

    basvuru = models.ForeignKey(Basvuru, on_delete=models.CASCADE, related_name='belgeler', verbose_name=_('Başvuru'))
    type = models.CharField(_('Tür'), max_length=10, choices=Type.choices)
    file = models.FileField(_('Dosya'), upload_to='belgeler/')
    upload_date = models.DateTimeField(_('Yükleme Tarihi'), auto_now_add=True)
    is_main_author = models.BooleanField(_('Birinci Yazar mı?'), default=False)
    category = models.CharField(_('Kategori'), max_length=2, choices=YayinKategori.choices, null=True, blank=True)
    description = models.TextField(_('Açıklama'), blank=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Belge')
        verbose_name_plural = _('Belgeler')
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.basvuru} - {self.get_type_display()}"

class Tablo5(models.Model):
    basvuru = models.OneToOneField(Basvuru, on_delete=models.CASCADE, related_name='tablo5', verbose_name=_('Başvuru'))
    creation_date = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    file_path = models.FileField(_('Dosya Yolu'), upload_to='tablo5_files/', null=True, blank=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Tablo 5')
        verbose_name_plural = _('Tablo 5\'ler')
        ordering = ['-creation_date']

    def __str__(self):
        return f"Tablo 5 - {self.basvuru}"

class Puan(models.Model):
    tablo5 = models.ForeignKey(Tablo5, on_delete=models.CASCADE, related_name='puanlar', verbose_name=_('Tablo 5'))
    kriter = models.ForeignKey(Kriter, on_delete=models.CASCADE, related_name='puanlar', verbose_name=_('Kriter'))
    value = models.DecimalField(_('Değer'), max_digits=5, decimal_places=2)
    supporting_documents = models.ManyToManyField(Belge, related_name='puanlar', verbose_name=_('Destekleyici Belgeler'))
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Puan')
        verbose_name_plural = _('Puanlar')
        ordering = ['kriter__ad']
        unique_together = ['tablo5', 'kriter']

    def __str__(self):
        return f"{self.tablo5} - {self.kriter.ad}: {self.value}"
