from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed # Import AuthenticationFailed
# from .serializers import CustomTokenObtainPairSerializer # Use the one below
from .models import BlacklistedToken
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout

from users.serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

# Define the custom serializer here as it's used by the view below
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        # Ensure tc_kimlik_no exists, provide default if not
        token['tc_kimlik_no'] = getattr(user, 'tc_kimlik_no', '') 
        token['email'] = user.email
        token['role'] = user.role
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token

    def validate(self, attrs):
        # Default validation first (handles username/password check)
        data = super().validate(attrs) 
        
        # Add user details to the response payload
        serializer = UserSerializer(self.user, context=self.context)
        data['user'] = serializer.data
        
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    JWT token ile giriş için özel view.
    Standart TokenObtainPairView davranışını kullanır, ancak token'a
    ve yanıta özel alanlar eklemek için CustomTokenObtainPairSerializer kullanır.
    TC Kimlik No ile giriş için, frontend'in TC'yi 'username' alanına göndermesi gerekir.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    
    # Removed the custom post method to rely on the parent class's implementation
    # which uses Django's authentication backend correctly.
    # The serializer_class handles adding custom claims and user data.

@swagger_auto_schema(
    methods=['post'],
    operation_summary="Kullanıcı çıkış işlemi",
    operation_description="Kullanıcı oturumunu sonlandırır ve token'ı geçersiz kılar",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Refresh Token')
        },
    ),
    responses={
        200: openapi.Response(description="Başarılı çıkış"),
        400: openapi.Response(description="Geçersiz veya eksik token"),
        401: openapi.Response(description="Yetkilendirme hatası")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Logout için kimlik doğrulaması gerekir
def logout_view(request):
    """
    Kullanıcı çıkış view'ı.
    JWT refresh token'ı blacklist'e ekler (eğer blacklist app kuruluysa).
    """
    print("[Logout] İstek alındı.") # Log
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            print("[Logout] Hata: Refresh token eksik.") # Log
            return Response({"detail": "Refresh token gerekli."}, status=status.HTTP_400_BAD_REQUEST)
        
        print("[Logout] Refresh token alındı, blacklist deneniyor...") # Log
        token = RefreshToken(refresh_token)
        token.blacklist() # Bu, blacklist app kuruluysa çalışır
        print("[Logout] Token başarıyla blacklist'e eklendi (veya blacklist aktif değil).") # Log
            
        return Response({"detail": "Başarıyla çıkış yapıldı."}, status=status.HTTP_200_OK)
    except TokenError as e:
        print(f"[Logout] TokenError: {str(e)}") # Log
        # Geçersiz token ile logout denemesi normal, 400 döndürebiliriz.
        return Response({"detail": f"Geçersiz token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Blacklist app kurulu değilse AttributeError verebilir, bunu yakalayalım
        if isinstance(e, AttributeError) and 'blacklist' in str(e):
             print("[Logout] Blacklist özelliği aktif değil, token blacklist'e eklenemedi.") # Log
             # Blacklist olmadan da çıkış başarılı sayılabilir
             return Response({"detail": "Çıkış yapıldı (blacklist aktif değil)."}, status=status.HTTP_200_OK)
        
        print(f"[Logout] Beklenmedik Hata: {str(e)}") # Log
        return Response({'detail': 'Çıkış sırasında bir hata oluştu.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    methods=['post'],
    operation_description="Yeni kullanıcı kaydı yapar",
    request_body=UserCreateSerializer, # Use serializer directly
    responses={
        201: UserSerializer, # Return full user details
        400: "Geçersiz veri"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Yeni kullanıcı kaydı yapar.
    """
    print("[Register] İstek alındı.") # Log
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data, context={'request': request}) # Pass context
        if serializer.is_valid():
            user = serializer.save()
            print(f"[Register] Kullanıcı başarıyla oluşturuldu: {user.username}") # Log
            # Return full user details using UserSerializer
            return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED) 
        print(f"[Register] Hata: Geçersiz veri: {serializer.errors}") # Log
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# login_view fonksiyonu users/views.py'den kaldırıldığı için burada da silebiliriz.
# Ancak import edildiği için hata vermemesi adına şimdilik kalabilir veya import'u kaldırılabilir.
# from users.views import login_view # Bu import kaldırılabilir.
