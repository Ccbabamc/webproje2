from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import TCAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from users.models import Admin, Yonetici, JuriUyesi

class TCObtainAuthToken(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TCAuthTokenSerializer
    throttle_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            # Debug logları
            print("Raw request data:", request.data)
            
            serializer = self.serializer_class(data=request.data)
            
            # TC kimlik veya username boş ise diğerinden doldur
            data = request.data.copy()
            if 'tc_kimlik_no' in data and data['tc_kimlik_no'] and not data.get('username'):
                data['username'] = data['tc_kimlik_no']
            elif 'username' in data and data['username'] and not data.get('tc_kimlik_no'):
                data['tc_kimlik_no'] = data['username']
            
            serializer = self.serializer_class(data=data)
            print("Processed request data:", data)
            
            if not serializer.is_valid():
                print("Serializer errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Kullanıcı bilgilerini hazırla
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'tc_kimlik_no': user.tc_kimlik_no,
                'email': user.email,
                'username': user.username
            }
            
            # Rol bilgisini ekle ve rol detaylarını hazırla
            if user.is_superuser:
                user_data['role'] = 'SUPERADMIN'
                user_data['department'] = 'Tüm Departmanlar'
                user_data['faculty'] = 'Tüm Fakülteler'
            elif user.role == 'ADMIN':
                user_data['role'] = 'ADMIN'
                try:
                    admin = Admin.objects.get(user=user)
                    user_data['department'] = admin.department
                except Admin.DoesNotExist:
                    user_data['department'] = user.department
            elif user.role == 'YONETICI':
                user_data['role'] = 'YONETICI'
                try:
                    yonetici = Yonetici.objects.get(user=user)
                    user_data['department'] = yonetici.department
                    user_data['faculty'] = yonetici.faculty
                except Yonetici.DoesNotExist:
                    user_data['department'] = user.department
                    user_data['faculty'] = user.faculty
            elif user.role == 'JURI_UYESI':
                user_data['role'] = 'JURI_UYESI'
                try:
                    juri = JuriUyesi.objects.get(user=user)
                    user_data['department'] = juri.department
                    user_data['faculty'] = juri.faculty
                    user_data['expertise'] = juri.expertise
                except JuriUyesi.DoesNotExist:
                    user_data['department'] = user.department
                    user_data['faculty'] = user.faculty
            else:
                user_data['role'] = user.role  # ADAY veya diğer roller
                
            return Response({
                'token': token.key,
                'user': user_data
            })
        except Exception as e:
            print(f"Login error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 