from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Aday, Admin, Yonetici, JuriUyesi

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name', 'email', 'role', 'phone', 'address')}),
        ('İzinler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Önemli tarihler', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Aday)
class AdayAdmin(admin.ModelAdmin):
    list_display = ('user', 'cv', 'diploma')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'department')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Yonetici)
class YoneticiAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'faculty')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'department', 'faculty')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JuriUyesi)
class JuriUyesiAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'department', 'faculty')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'expertise', 'department', 'faculty')
    readonly_fields = ('created_at', 'updated_at')
