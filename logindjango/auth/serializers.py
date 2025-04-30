from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT token için özel serializer.
    TC kimlik numarası ve username girişlerini destekler.
    """
    tc_kimlik_no = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        # Debug mesajları
        print("CustomTokenObtainPairSerializer.validate() attrs:", attrs)
        
        # TC Kimlik veya username kontrolü
        username_field = User.USERNAME_FIELD
        print(f"USERNAME_FIELD: {username_field}")
        
        # Önce tc_kimlik_no değeri aranır, yoksa username değerine bakılır
        tc_kimlik = attrs.get('tc_kimlik_no')
        username_val = attrs.get('username')
        
        print(f"tc_kimlik_no: {tc_kimlik}, username: {username_val}")
        
        # Eğer tc_kimlik_no verildiyse, bunu kullan
        if tc_kimlik:
            username = tc_kimlik
        # Eğer username verildiyse, bunu kullan
        elif username_val:
            username = username_val
        else:
            username = None
            
        print(f"Final username to use: {username}")
        
        if not username:
            print("Username validation error: No username or tc_kimlik_no provided")
            raise serializers.ValidationError({
                "detail": _("Kullanıcı adı veya TC Kimlik No gerekli."),
            })
        
        # Şifre kontrolü
        password = attrs.get('password')
        if not password:
            print("Password validation error: No password provided")
            raise serializers.ValidationError({
                "detail": _("Şifre gerekli."),
            })
        
        # Django auth için username field'ına değeri set et
        attrs[username_field] = username
        
        # Eğer User.USERNAME_FIELD 'username' ise ve attrs'da 'tc_kimlik_no' yoksa, 
        # bunun da username ile aynı değere set edildiğinden emin ol
        if username_field == 'username' and not 'tc_kimlik_no' in attrs:
            attrs['tc_kimlik_no'] = username
            
        print(f"Final attrs for authentication: {attrs}")

        # Kullanıcıyı bul
        try:
            # authenticate fonksiyonuna User.USERNAME_FIELD'a uygun parametre geçir
            auth_kwargs = {
                'request': self.context.get('request'),
                username_field: username,
                'password': password
            }
            user = authenticate(**auth_kwargs)
            
            if not user:
                # Alternatif olarak tc_kimlik_no ile dene
                if username_field != 'tc_kimlik_no':
                    user = authenticate(
                        request=self.context.get('request'),
                        tc_kimlik_no=username,
                        password=password
                    )
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            user = None

        print(f"Authentication result: {'Success' if user else 'Failed'}")

        if not user:
            print(f"Authentication failed for username: {username}")
            raise serializers.ValidationError({
                "detail": _("Kullanıcı adı veya şifre hatalı."),
            })

        # Süper kullanıcılar için özel kontrol (Django superuser)
        if user.is_superuser:
            # User nesnesini view tarafından erişim için kaydet
            self.user = user
            
            # JWT token oluştur
            refresh = self.get_token(user)
            
            # Kullanıcı rolünü güvenli bir şekilde al
            user_role = getattr(user, 'role', 'ADMIN')
            
            # Dönüş değerini hazırla
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'tc_kimlik_no': getattr(user, 'tc_kimlik_no', user.username),
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user_role,
                    'is_superuser': True
                }
            }
        
        # Normal kullanıcı işlemleri
        if not user.is_active:
            raise serializers.ValidationError({
                "detail": _("Hesabınız devre dışı bırakılmış."),
            })
            
        # User nesnesini view tarafından erişim için kaydet
        self.user = user
        
        # TokenObtainPairSerializer'ın validate metodu çağrılır
        attrs['user'] = user
        data = super().validate(attrs)
        
        return data
        
    @classmethod
    def get_token(cls, user):
        return super().get_token(user) 