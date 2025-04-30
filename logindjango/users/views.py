from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .models import Aday, Admin, Yonetici, JuriUyesi, User # Import User explicitly
from .serializers import (
    UserSerializer,
    AdaySerializer,
    AdminSerializer,
    YoneticiSerializer,
    JuriUyesiSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)
from .permissions import IsAdmin, IsYonetici, IsJuriUyesi, IsAday, IsOwnerOrAdmin, IsAdminOrYonetici # Import IsAdminOrYonetici
from rest_framework.exceptions import AuthenticationFailed, ValidationError # Import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# User = get_user_model() # Already imported above

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined') # Default ordering
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'register': 
             permission_classes = [AllowAny]
        elif self.action == 'create': 
             permission_classes = [IsAdminUser] # Only staff/superadmins can create via this standard method
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
             # Allow staff/superadmin OR owner (though owner logic might be complex here)
             # Using IsAdminUser is simpler for admin actions on any user.
             permission_classes = [IsAuthenticated, IsAdminUser] 
        elif self.action in ['me', 'me_update']:
             permission_classes = [IsAuthenticated]
        elif self.action == 'list': 
             # Allow staff/superadmin OR users with the ADMIN role
             if self.request.user.is_staff or (hasattr(self.request.user, 'role') and self.request.user.role == User.Role.ADMIN):
                 permission_classes = [permissions.IsAuthenticated]
             else:
                 # Deny access if not staff or ADMIN role
                 permission_classes = [IsAdminUser] # This will effectively deny non-staff/non-ADMIN
        else: 
            # Default to staff/superuser for any other actions
            permission_classes = [IsAdminUser] 
            
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'register':
            return UserCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update': 
            return UserUpdateSerializer
        elif self.action == 'me_update': 
            return UserUpdateSerializer 
        return UserSerializer 

    def get_queryset(self):
        """
        Return appropriate queryset based on the action.
        Permissions (checked in get_permissions) handle authorization.
        """
        user = self.request.user
        # Basic check for authentication
        if not user.is_authenticated:
            return User.objects.none()

        # Let permissions handle who can list. If allowed, show all.
        return User.objects.all().order_by('-date_joined') 

    @swagger_auto_schema(
        methods=['post'],
        operation_description="Yeni kullanıcı kaydı yapar (Public registration)",
        request_body=UserCreateSerializer, # Use serializer directly
        responses={
            201: UserSerializer, # Return full user details on success
            400: "Geçersiz veri"
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Yeni kullanıcı kaydı yapar (Public).
        Sets role to ADAY by default if not provided or invalid.
        """
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            # Ensure role is set, default to ADAY if needed during creation
            role = serializer.validated_data.get('role')
            if not role or role not in [r[0] for r in User.Role.choices]:
                 serializer.validated_data['role'] = User.Role.ADAY # Default to ADAY for public registration
                 
            user = serializer.save()
            # Return the standard UserSerializer data
            return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
             return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             print(f"Registration error: {str(e)}")
             return Response({"error": f"Kayıt sırasında bir hata oluştu: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Standard create method for Admins (Superusers/Staff)
    @swagger_auto_schema(
        operation_description="Yeni kullanıcı oluşturur (Admin/Superuser only)",
        request_body=UserCreateSerializer,
        responses={201: UserSerializer, 400: "Geçersiz Veri", 403: "Yetki Reddedildi"}
    )
    def create(self, request, *args, **kwargs):
        """
        Yeni kullanıcı oluşturma (Admin/Superuser yetkisi gerektirir).
        Allows setting any role. Model's save method handles setting is_staff based on role.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save() 
            headers = self.get_success_headers(serializer.data)
            # Return standard user details
            return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Admin user creation error: {str(e)}")
            # Check for unique constraint errors specifically
            if 'unique constraint' in str(e).lower():
                 error_field = 'email' if 'email' in str(e).lower() else 'tc_kimlik_no' if 'tc_kimlik_no' in str(e).lower() else 'username' if 'username' in str(e).lower() else 'unknown'
                 # Provide a more specific error message structure
                 return Response({error_field: [f"Bu {error_field} zaten kullanımda."]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": f"Kullanıcı oluşturulamadı: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        methods=['get'],
        operation_description="Giriş yapmış kullanıcının bilgilerini döndürür",
        responses={ 200: UserSerializer, 401: "Kimlik doğrulama hatası" }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated]) 
    def me(self, request):
        """
        Giriş yapmış kullanıcının bilgilerini döndürür.
        """
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
        
    @swagger_auto_schema(
        methods=['put', 'patch'], # Allow PATCH for partial updates
        operation_description="Giriş yapmış kullanıcının bilgilerini günceller",
        request_body=UserUpdateSerializer,
        responses={ 200: UserSerializer, 400: "Geçersiz veri", 401: "Kimlik doğrulama hatası" }
    )
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated]) 
    def me_update(self, request):
        """
        Giriş yapmış kullanıcının bilgilerini günceller. PUT veya PATCH destekler.
        """
        user = request.user
        partial = request.method == 'PATCH' 
        serializer = UserUpdateSerializer(user, data=request.data, partial=partial, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            updated_user = serializer.save()
            # Return full user details after update
            return Response(UserSerializer(updated_user, context={'request': request}).data)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             print(f"User self-update error: {str(e)}")
             return Response({"error": f"Profil güncellenirken bir hata oluştu: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Override update/partial_update for admin actions on specific users
    @swagger_auto_schema(
        operation_description="Belirtilen kullanıcının bilgilerini günceller (Admin/Superuser only)",
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer, 400: "Geçersiz Veri", 403: "Yetki Reddedildi", 404: "Bulunamadı"}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object() # Gets user by pk, handles 404
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # Return full user details after update
            return Response(UserSerializer(instance, context={'request': request}).data)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             return Response({"error": f"Kullanıcı güncellenirken bir hata oluştu: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # perform_create and perform_update are implicitly handled by serializer.save()

    # Explicitly define destroy (based on previous fix, without debug logs)
    @swagger_auto_schema(
        operation_description="Belirtilen kullanıcıyı siler (Admin/Superuser only)",
        responses={204: "Başarıyla Silindi", 403: "Yetki Reddedildi", 404: "Bulunamadı"}
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object() # Retrieve the object, handles 404
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e: 
            raise e # Re-raise the exception to let DRF handle the response

    def perform_destroy(self, instance):
        """Perform the deletion."""
        instance.delete()


# --- Role Specific ViewSets (Keep as is or refactor if needed) ---
# These seem less relevant to the current user listing/creation issue for admins

class AdayViewSet(viewsets.ModelViewSet):
    queryset = Aday.objects.all()
    serializer_class = AdaySerializer
    permission_classes = [permissions.IsAuthenticated] # Base permission

    def get_permissions(self):
        if self.action in ['list']:
            return [IsAdminUser()] # Use standard Django admin permission
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()] # Assumes IsOwnerOrAdmin checks Aday.user
        return [permissions.IsAuthenticated()] 

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Aday.objects.none()
            
        if user.is_superuser or (hasattr(user, 'role') and user.role in ['ADMIN', 'YONETICI']):
            return Aday.objects.all()
        elif hasattr(user, 'role') and user.role == 'ADAY':
            return Aday.objects.filter(user=user)
        
        return Aday.objects.none() # Default deny

class AdminViewSet(viewsets.ReadOnlyModelViewSet): # Usually Admins aren't managed via API like this
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser] # Only admins can view admin profiles

class YoneticiViewSet(viewsets.ReadOnlyModelViewSet): # Usually Managers aren't managed via API like this
    queryset = Yonetici.objects.all()
    serializer_class = YoneticiSerializer
    permission_classes = [IsAdminUser] # Only admins can view manager profiles

class JuriUyesiViewSet(viewsets.ModelViewSet): # Jury members might be managed
    queryset = JuriUyesi.objects.all()
    serializer_class = JuriUyesiSerializer
    permission_classes = [IsAdminUser] # Only Admins can manage Jury members

# --- Authentication Views (Keep as is) ---
# CustomTokenObtainPairView is now in auth/views.py
