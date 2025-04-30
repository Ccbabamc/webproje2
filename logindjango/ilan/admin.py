from django.contrib import admin
from .models import Fakulte, Bolum, Kriter, Ilan

@admin.register(Fakulte)
class FakulteAdmin(admin.ModelAdmin):
    list_display = ('ad', 'created_at', 'updated_at')
    search_fields = ('ad',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Bolum)
class BolumAdmin(admin.ModelAdmin):
    list_display = ('ad', 'fakulte', 'created_at', 'updated_at')
    list_filter = ('fakulte',)
    search_fields = ('ad', 'fakulte__ad')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Kriter)
class KriterAdmin(admin.ModelAdmin):
    list_display = ('ad', 'puan', 'created_at', 'updated_at')
    search_fields = ('ad', 'aciklama')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Ilan)
class IlanAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'bolum', 'son_basvuru_tarihi', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'bolum__fakulte', 'bolum')
    search_fields = ('baslik', 'aciklama', 'bolum__ad', 'bolum__fakulte__ad')
    filter_horizontal = ('kriterler',)
    readonly_fields = ('created_at', 'updated_at')
