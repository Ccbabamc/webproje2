from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet,
    AdayViewSet,
    AdminViewSet,
    YoneticiViewSet,
    JuriUyesiViewSet
    # CustomTokenObtainPairView # Removed import from here, it's in auth/views.py
    # login_view # Removed import for the deleted function
)
# Import it from the correct location if needed elsewhere, but not needed for these urlpatterns
# from auth.views import CustomTokenObtainPairView 

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'adaylar', AdayViewSet)
router.register(r'adminler', AdminViewSet)
router.register(r'yoneticiler', YoneticiViewSet)
router.register(r'juri-uyeleri', JuriUyesiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # JWT Token
    # path('login/', login_view, name='token_obtain_pair'), # Removed redundant login view URL
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Kullanıcı kaydı için açık endpoint
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('me/', UserViewSet.as_view({'get': 'me', 'put': 'me_update'}), name='me'),
    
    # Profil fotoğrafı yükleme endpoint'i
    path('upload-profile-photo/', UserViewSet.as_view({'post': 'upload_profile_photo'}), name='upload_profile_photo'),
]
