from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        YONETICI = 'YONETICI', _('Yönetici')
        JURI_UYESI = 'JURI_UYESI', _('Jüri Üyesi')
        ADAY = 'ADAY', _('Aday')
        SUPERADMIN = 'SUPERADMIN', _('Super Admin')

    username = models.CharField(max_length=11, unique=True, verbose_name=_('TC Kimlik No'))
    tc_kimlik_no = models.CharField(max_length=11, verbose_name=_('TC Kimlik No'), default='')
    email = models.EmailField(_('E-posta adresi'), blank=True)
    role = models.CharField(_('Rol'), max_length=20, choices=Role.choices, default=Role.ADAY)
    phone = models.CharField(_('Telefon'), max_length=15, blank=True)
    address = models.TextField(_('Adres'), blank=True)
    department = models.CharField(_('Bölüm'), max_length=100, blank=True)
    faculty = models.CharField(_('Fakülte'), max_length=100, blank=True)
    created_at = models.DateTimeField(_('Oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme tarihi'), auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('Kullanıcı')
        verbose_name_plural = _('Kullanıcılar')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['tc_kimlik_no'],
                name='unique_tc_kimlik_no',
                condition=models.Q(tc_kimlik_no__isnull=False) & ~models.Q(tc_kimlik_no='')
            ),
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email',
                condition=models.Q(email__isnull=False) & ~models.Q(email='')
            )
        ]

    def __str__(self):
        # Handle cases where first_name or last_name might be None or empty
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        tc = self.tc_kimlik_no or self.username or 'No TC/Username'
        return f"{full_name} ({tc})" if full_name else tc


    def save(self, *args, **kwargs):
        # TC kimlik ve username senkronizasyonu (önce yapalım)
        if not self.username and self.tc_kimlik_no:
            self.username = self.tc_kimlik_no
        
        # Rol ve yetki ayarlamaları
        if self.is_superuser:
            self.role = self.Role.SUPERADMIN
            self.is_staff = True # Superuser her zaman staff olmalı
        elif self.role == self.Role.ADMIN:
             self.is_staff = True # Admin rolü staff olmalı
        else:
             # Diğer roller (YONETICI, JURI_UYESI, ADAY) staff olmamalı
             # (Eğer superuser değilse)
             if not self.is_superuser: 
                 self.is_staff = False 
        
        super().save(*args, **kwargs)

class Aday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aday_profile')
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    diploma = models.FileField(upload_to='diploma/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name=_('Profil Fotoğrafı'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Aday')
        verbose_name_plural = _('Adaylar')
        ordering = ['-created_at']

    def __str__(self):
        return self.user.get_full_name() if self.user else 'No User Linked'


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Adminler')
        ordering = ['-created_at']

    def __str__(self):
        return self.user.get_full_name() if self.user else 'No User Linked'


class Yonetici(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='yonetici_profile')
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Yönetici')
        verbose_name_plural = _('Yöneticiler')
        ordering = ['-created_at']

    def __str__(self):
        return self.user.get_full_name() if self.user else 'No User Linked'


class JuriUyesi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='juri_uyesi_profile')
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    expertise = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Jüri Üyesi')
        verbose_name_plural = _('Jüri Üyeleri')
        ordering = ['-created_at']

    def __str__(self):
        return self.user.get_full_name() if self.user else 'No User Linked'
