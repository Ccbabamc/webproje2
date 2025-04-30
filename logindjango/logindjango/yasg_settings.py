from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.permissions import AllowAny
from django.urls import path, include
import json
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.serializers import Serializer, ModelSerializer
from django.core.serializers.json import DjangoJSONEncoder
import inspect
from drf_yasg.codecs import OpenAPICodecJson
from rest_framework import serializers
from django.utils.encoding import force_bytes
from types import SimpleNamespace

# Serializer sorunu için monkey patch oluşturuyoruz
def patched_replace_serializer(obj):
    """
    Serializer sınıflarını string temsilleri ile değiştir
    """
    if inspect.isclass(obj) and issubclass(obj, serializers.Serializer):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title=f"{obj.__name__}",
            description=f"Serializer: {obj.__name__}"
        )
    if isinstance(obj, serializers.Serializer):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title=f"{obj.__class__.__name__}",
            description=f"Serializer: {obj.__class__.__name__}"
        )
    return obj

# JSON encoder'ı düzelt
original_default = json.JSONEncoder.default

def patched_default(self, obj):
    obj = patched_replace_serializer(obj)
    try:
        return original_default(self, obj)
    except TypeError:
        try:
            # Diğer serialize edilemeyen nesneleri stringe dönüştür
            return str(obj)
        except:
            return "<Tidak Dapat Dikonversi>"

# Patch uygula
json.JSONEncoder.default = patched_default

# Özelleştirilmiş Swagger Auto Schema
class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_request_body_schema(self, serializer):
        try:
            return super().get_request_body_schema(serializer)
        except Exception as e:
            if hasattr(serializer, 'get_fields'):
                # Manuel şema oluştur
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={},
                )
                return schema
            return None

# Özelleştirilmiş OpenAPI Şema Çözücü
class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        try:
            schema = super().get_schema(request, public)
            # Swagger UI'da gösterilecek ekstra bilgiler
            schema.basePath = '/api'  # Tüm API'ler /api ile başlar
            return schema
        except Exception as e:
            # Hata durumunda temel şema oluştur
            return SimpleNamespace(
                basePath='/api',
                paths={},
                info=SimpleNamespace(
                    title="API Şeması Oluşturulamadı",
                    description=f"Hata: {str(e)}",
                    version="1.0"
                )
            )

# Özel OpenAPI codec sınıfı
class SafeOpenAPICodecJson(OpenAPICodecJson):
    def _dump_dict(self, spec):
        """Dump ``spec`` into JSON."""
        try:
            if self.pretty:
                return f"{json.dumps(spec, indent=4, default=lambda o: str(o), separators=(',', ': '), ensure_ascii=False)}\n"
            return json.dumps(spec, default=lambda o: str(o), ensure_ascii=False)
        except Exception as e:
            # Hata durumunda basit JSON döndür
            return json.dumps({"error": f"Schema JSON serialization error: {str(e)}"})

# OpenAPICodecJson sınıfını monkey patch ile değiştir
OpenAPICodecJson._dump_dict = SafeOpenAPICodecJson._dump_dict

# Swagger Şema Görünümünü Oluştur
schema_view = get_schema_view(
    openapi.Info(
        title="Kocaeli Üniversitesi Akademik Personel Başvuru Sistemi API",
        default_version='v1.0',
        description="""
        Kocaeli Üniversitesi Akademik Personel Başvuru Sistemi için RESTful API.
        
        ## Kimlik Doğrulama
        API'ye erişim için JWT kimlik doğrulama kullanılmaktadır. İstek başlığında 'Authorization: Bearer YOUR_TOKEN' şeklinde token kullanılmalıdır.
        
        ## Kullanıcı Rolleri
        * SUPERADMIN: Sistem yöneticisi (tüm yetkilere sahip)
        * ADMIN: Normal yönetici (çoğu işlevi yapabilir)
        * YONETICI: Bölüm/Fakülte yöneticisi
        * JURI_UYESI: Değerlendirme komitesi üyesi
        * ADAY: Başvuru yapan akademik personel adayı
        """,
        terms_of_service="https://www.kocaeli.edu.tr/terms/",
        contact=openapi.Contact(email="akademik@kocaeli.edu.tr"),
        license=openapi.License(name="Kocaeli Üniversitesi Lisansı"),
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
    patterns=[
        path('api/auth/', include('auth.urls')),
        path('api/users/', include('users.urls')),
        path('api/announcements/', include('ilan.urls')),
        path('api/applications/', include('basvuru.urls')),
    ],
    generator_class=CustomOpenAPISchemaGenerator,
) 