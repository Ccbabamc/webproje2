from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Aday, Admin, Yonetici, JuriUyesi

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'ADAY':
            Aday.objects.create(user=instance)
        elif instance.role == 'ADMIN':
            Admin.objects.create(user=instance)
        elif instance.role == 'YONETICI':
            Yonetici.objects.create(user=instance)
        elif instance.role == 'JURI_UYESI':
            JuriUyesi.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'ADAY':
        Aday.objects.get_or_create(user=instance)
    elif instance.role == 'ADMIN':
        Admin.objects.get_or_create(user=instance)
    elif instance.role == 'YONETICI':
        Yonetici.objects.get_or_create(user=instance)
    elif instance.role == 'JURI_UYESI':
        JuriUyesi.objects.get_or_create(user=instance) 