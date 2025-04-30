from django.urls import resolve
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

class SwaggerPermissionMiddleware:
    """
    Swagger URL'leri için özel izin sınıfı.
    Swagger erişimini yetkilendirme olmadan sağlar.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # İstek path kontrolü
        if request.path.startswith('/swagger/') or request.path.startswith('/redoc/'):
            request.swagger_request = True
            
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # View fonksiyonu kontrolü
        if getattr(request, 'swagger_request', False):
            # Swagger sayfaları için izinleri AllowAny olarak ayarla
            view_func.cls.permission_classes = [AllowAny]
            view_func.cls.authentication_classes = []
        return None 