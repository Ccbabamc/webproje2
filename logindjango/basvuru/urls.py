# logindjango/basvuru/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BasvuruViewSet, BelgeViewSet, Tablo5ViewSet, PuanViewSet

router = DefaultRouter()
router.register(r'applications', BasvuruViewSet)
router.register(r'documents', BelgeViewSet)
router.register(r'table5', Tablo5ViewSet)
router.register(r'scores', PuanViewSet)

# Özel belge endpoint'leri
document_list = BelgeViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

document_detail = BelgeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

document_my = BelgeViewSet.as_view({
    'get': 'my'
})

document_upload = BelgeViewSet.as_view({
    'post': 'upload'
})

urlpatterns = [
    path('', include(router.urls)),
    # El ile eklediğimiz my endpointi, doğrudan my/ şeklinde
    path('my/', BasvuruViewSet.as_view({'get': 'my'}), name='basvuru-my'),
    path('documents/my/', BelgeViewSet.as_view({'get': 'my'}), name='belge-my'),
    # Ana listeler için URL'ler
    path('basvurular/', BasvuruViewSet.as_view({'get': 'list'}), name='basvuru-list'),
    path('basvurular/<pk>/', BasvuruViewSet.as_view({'get': 'retrieve'}), name='basvuru-detail'),
    path('basvurular/aday/<pk>/', BasvuruViewSet.as_view({'get': 'aday_basvurulari'}), name='aday-basvurulari'),
    path('basvurular/my/', BasvuruViewSet.as_view({'get': 'my'}), name='my-basvurular'),
    path('belgeler/', document_list, name='belge-list'),
    path('belgeler/<pk>/', document_detail, name='belge-detail'),
    path('belgeler/my/', document_my, name='my-belgeler'),
    path('belgeler/upload/', document_upload, name='upload-belge'),
]