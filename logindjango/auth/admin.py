from django.contrib import admin
from .models import BlacklistedToken

@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_preview', 'timestamp')
    search_fields = ('token',)
    readonly_fields = ('timestamp',)
    
    def token_preview(self, obj):
        return f"{obj.token[:20]}..."
    
    token_preview.short_description = 'Token'
