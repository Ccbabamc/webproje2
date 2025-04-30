from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FakulteViewSet, BolumViewSet, KriterViewSet, IlanViewSet

# API v1 için router
router_v1 = DefaultRouter()
router_v1.register(r'faculties', FakulteViewSet)
router_v1.register(r'departments', BolumViewSet)
router_v1.register(r'criteria', KriterViewSet)
router_v1.register(r'', IlanViewSet)

# Frontend uyumluluğu için özel endpoint'ler
urlpatterns = [
    # API v1
    path('v1/', include(router_v1.urls)),
    
    # Frontend uyumlu endpoint'ler
    path('fakulteler/', FakulteViewSet.as_view({'get': 'list'}), name='fakulteler-list'),
    path('bolumler/', BolumViewSet.as_view({'get': 'list'}), name='bolumler-list'),
    
    # Legacy support
    path('', include(router_v1.urls)),
]
