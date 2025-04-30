from django.db import models

# Create your models here.

class BlacklistedToken(models.Model):
    """
    JWT blacklist modeli.
    Geçersiz kılınan(logout olan) JWT tokenlarını tutar.
    """
    token = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token[:10]}... - {self.timestamp}"
    
    class Meta:
        verbose_name = "Blacklisted Token"
        verbose_name_plural = "Blacklisted Tokens"
