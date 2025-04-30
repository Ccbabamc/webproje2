from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Fakulte(models.Model):
    ad = models.CharField(_('Ad'), max_length=255)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Fakülte')
        verbose_name_plural = _('Fakülteler')
        ordering = ['ad']

    def __str__(self):
        return self.ad

class Bolum(models.Model):
    # Fakülte ilişkisini isteğe bağlı hale getiriyoruz (null=True, blank=True)
    # on_delete=models.SET_NULL: Eğer ilişkili fakülte silinirse, bölümün fakülte alanı NULL olarak ayarlanır.
    # Alternatif olarak on_delete=models.PROTECT kullanılabilir, bu durumda ilişkili bölüm varken fakülte silinemez.
    # Şimdilik SET_NULL daha esnek görünüyor.
    fakulte = models.ForeignKey(Fakulte, on_delete=models.SET_NULL, related_name='bolumler', verbose_name=_('Fakülte'), null=True, blank=True)
    ad = models.CharField(_('Ad'), max_length=255)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Bölüm')
        verbose_name_plural = _('Bölümler')
        # Fakülte artık null olabileceğinden, sıralamayı sadece 'ad' a göre yapalım veya fakülte null ise farklı bir mantık kuralım.
        # Şimdilik sadece 'ad' a göre sıralayalım.
        ordering = ['ad']

    def __str__(self):
        # Fakülte null olabileceğinden, __str__ metodunu güncelleyelim.
        if self.fakulte:
            return f"{self.fakulte.ad} - {self.ad}"
        return self.ad

class Kriter(models.Model):
    ad = models.CharField(_('Ad'), max_length=255)
    aciklama = models.TextField(_('Açıklama'), blank=True)
    puan = models.DecimalField(_('Puan'), max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Kriter')
        verbose_name_plural = _('Kriterler')
        ordering = ['ad']

    def __str__(self):
        return f"{self.ad} ({self.puan} puan)"

class Ilan(models.Model):
    class Status(models.TextChoices):
        TASLAK = 'TASLAK', _('Taslak')
        AKTIF = 'AKTIF', _('Aktif')
        KAPALI = 'KAPALI', _('Kapalı')

    bolum = models.ForeignKey(Bolum, on_delete=models.CASCADE, related_name='ilanlar', verbose_name=_('Bölüm'))
    baslik = models.CharField(_('Başlık'), max_length=255)
    aciklama = models.TextField(_('Açıklama'))
    son_basvuru_tarihi = models.DateTimeField(_('Son Başvuru Tarihi'))
    status = models.CharField(_('Durum'), max_length=10, choices=Status.choices, default=Status.TASLAK)
    kriterler = models.ManyToManyField(Kriter, related_name='ilanlar', verbose_name=_('Kriterler'))
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('İlan')
        verbose_name_plural = _('İlanlar')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bolum} - {self.baslik}"
