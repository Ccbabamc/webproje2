from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Basvuru, Belge, Tablo5, Puan
from .serializers import (
    BasvuruListSerializer,
    BasvuruDetailSerializer,
    BasvuruCreateSerializer,
    BelgeSerializer,
    Tablo5Serializer,
    PuanSerializer,
)
from users.permissions import IsAdmin, IsYonetici, IsJuriUyesi, IsAday, IsOwnerOrAdmin

class BasvuruViewSet(viewsets.ModelViewSet):
    queryset = Basvuru.objects.all()
    serializer_class = BasvuruListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['ilan', 'status']

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAday()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        elif self.action in ['evaluate']:
            return [IsJuriUyesi()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return BasvuruCreateSerializer
        elif self.action == 'retrieve':
            return BasvuruDetailSerializer
        return BasvuruListSerializer

    def perform_create(self, serializer):
        # Mevcut kullanıcıyı başvurunun aday alanına otomatik ata
        serializer.save(aday=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        
        # Superuser için tüm verilere erişim izni
        if user.is_superuser:
            return self.queryset.all()
            
        if not hasattr(user, 'role'):
            return self.queryset.none()
            
        if user.role == 'ADAY':
            return self.queryset.filter(aday=user)
        elif user.role in ['ADMIN', 'YONETICI']:
            return self.queryset.all()
        elif user.role == 'JURI_UYESI':
            return self.queryset.filter(ilan__juri_uyeleri__user=user)
        return self.queryset.none()

    @action(detail=False, methods=['get'], url_path='my')
    def my(self, request):
        """
        Kullanıcının kendi başvurularını listeler.
        Bu endpoint, frontend'den gelen 'my' API çağrılarını karşılamak için eklenmiştir.
        Superuser için tüm başvurular gösterilir.
        """
        user = request.user
        
        # Superuser kontrolü - superuser her zaman her şeye erişebilir
        if user.is_superuser:
            queryset = self.queryset.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        if not hasattr(user, 'role'):
            return Response(
                {'error': 'Kullanıcı rolü bulunamadı.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if user.role == 'ADAY':
            queryset = self.queryset.filter(aday=user)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif user.role in ['ADMIN', 'YONETICI']:
            # Yönetici ve admin de tüm başvuruları görebilsin
            queryset = self.queryset.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Bu endpoint sadece adaylar, adminler ve yöneticiler tarafından kullanılabilir.'},
                status=status.HTTP_403_FORBIDDEN
            )

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        basvuru = self.get_object()
        if basvuru.status != 'DRAFT':
            return Response(
                {'error': 'Sadece taslak başvurular gönderilebilir.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        basvuru.status = 'SUBMITTED'
        basvuru.save()
        return Response({'status': 'Başvuru başarıyla gönderildi.'})

    @action(detail=True, methods=['post'])
    def evaluate(self, request, pk=None):
        basvuru = self.get_object()
        if basvuru.status != 'SUBMITTED':
            return Response(
                {'error': 'Sadece gönderilmiş başvurular değerlendirilebilir.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Değerlendirme mantığı burada uygulanacak
        basvuru.status = 'EVALUATED'
        basvuru.save()
        return Response({'status': 'Başvuru değerlendirildi.'})

class BelgeViewSet(viewsets.ModelViewSet):
    queryset = Belge.objects.all()
    serializer_class = BelgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        if not self.request.user.is_authenticated:
            return self.queryset.none()
            
        # Superuser için tüm verilere erişim sağla
        if self.request.user.is_superuser:
            return self.queryset.all()
            
        if not hasattr(self.request.user, 'role'):
            return self.queryset.none()
            
        if self.request.user.role == 'ADAY':
            return self.queryset.filter(basvuru__aday=self.request.user)
        elif self.request.user.role in ['ADMIN', 'YONETICI']:
            return self.queryset.all()
        elif self.request.user.role == 'JURI_UYESI':
            return self.queryset.filter(basvuru__status='SUBMITTED')
        return self.queryset.none()
        
    @action(detail=False, methods=['get'], url_path='my')
    def my(self, request):
        """
        Kullanıcının kendi belgelerini listeler.
        Bu endpoint, frontend'den gelen 'my' API çağrılarını karşılamak için eklenmiştir.
        """
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {'error': 'Oturum açmanız gerekiyor.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        if not hasattr(user, 'role'):
            return Response(
                {'error': 'Kullanıcı rolü bulunamadı.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if user.role == 'ADAY':
            queryset = self.queryset.filter(basvuru__aday=user)
            
            # Belgeler dizisini güzelce oluştur ve doğrudan döndür
            belge_listesi = []
            for belge in queryset:
                belge_item = {
                    'id': belge.id,
                    'title': belge.description or f"{belge.get_type_display()} Belgesi",
                    'type': belge.type,
                    'fileUrl': request.build_absolute_uri(belge.file.url) if belge.file else None,
                    'uploadDate': belge.upload_date.isoformat() if belge.upload_date else belge.created_at.isoformat(),
                    'status': 'active',  # Varsayılan durum
                    'size': belge.file.size if belge.file else 0,
                    'mimeType': belge.file.name.split('.')[-1] if belge.file and '.' in belge.file.name else ''
                }
                belge_listesi.append(belge_item)
            
            # Direkt olarak liste döndür, frontend isteğine uygun
            return Response(belge_listesi)
            
        elif user.role in ['ADMIN', 'YONETICI', 'SUPERADMIN'] or user.is_superuser:
            queryset = self.queryset.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Bu endpoint sadece adaylar, adminler ve yöneticiler tarafından kullanılabilir.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        """
        Belge yükleme endpoint'i. 
        Multipart form data ile belge yüklemek için kullanılır.
        """
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Oturum açmanız gerekiyor.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Formdan gelen verileri al
        file = request.FILES.get('file')
        basvuru_id = request.data.get('basvuru')
        belge_type = request.data.get('type')
        description = request.data.get('description')
        
        # Gerekli alanları kontrol et
        if not file:
            return Response(
                {'error': 'Dosya eksik.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not basvuru_id:
            return Response(
                {'error': 'Başvuru ID eksik.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not belge_type:
            return Response(
                {'error': 'Belge türü eksik.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Başvuruyu kontrol et
        try:
            basvuru = Basvuru.objects.get(id=basvuru_id)
            
            # Yalnızca kullanıcının kendi başvurularına belge eklemesine izin ver
            if basvuru.aday != request.user and not request.user.is_superuser and not request.user.role in ['ADMIN', 'YONETICI']:
                return Response(
                    {'error': 'Bu başvuruya belge eklemek için yetkiniz yok.'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Belgeyi oluştur
            belge = Belge.objects.create(
                basvuru=basvuru,
                type=belge_type,
                file=file,
                description=description
            )
            
            # YAYIN türünde ek alanları ekle
            if belge_type == 'YAYIN':
                is_main_author = request.data.get('is_main_author', False)
                category = request.data.get('category')
                
                belge.is_main_author = is_main_author == 'true' or is_main_author == True
                if category:
                    belge.category = category
                
                belge.save()
                
            # Başarılı yanıt
            return Response({
                'success': True,
                'message': 'Belge başarıyla yüklendi.',
                'document': {
                    'id': belge.id,
                    'title': belge.description or f"{belge.get_type_display()} Belgesi",
                    'type': belge.type,
                    'fileUrl': request.build_absolute_uri(belge.file.url) if belge.file else None,
                    'uploadDate': belge.upload_date.isoformat() if belge.upload_date else belge.created_at.isoformat(),
                    'status': 'active',
                    'size': belge.file.size if belge.file else 0,
                    'mimeType': belge.file.name.split('.')[-1] if belge.file and '.' in belge.file.name else ''
                }
            })
            
        except Basvuru.DoesNotExist:
            return Response(
                {'error': 'Belirtilen başvuru bulunamadı.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Belge yüklenirken bir hata oluştu: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class Tablo5ViewSet(viewsets.ModelViewSet):
    queryset = Tablo5.objects.all()
    serializer_class = Tablo5Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        # Superuser kontrolü
        if self.request.user.is_superuser:
            return self.queryset.all()
            
        if not hasattr(self.request.user, 'role'):
            return self.queryset.none()
            
        if self.request.user.role == 'ADAY':
            return self.queryset.filter(basvuru__aday=self.request.user)
        elif self.request.user.role in ['ADMIN', 'YONETICI']:
            return self.queryset.all()
        elif self.request.user.role == 'JURI_UYESI':
            return self.queryset.filter(basvuru__status='SUBMITTED')
        return self.queryset.none()

class PuanViewSet(viewsets.ModelViewSet):
    queryset = Puan.objects.all()
    serializer_class = PuanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsJuriUyesi()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        if not self.request.user.is_authenticated:
            return self.queryset.none()
            
        if not hasattr(self.request.user, 'role'):
            return self.queryset.none()
            
        if self.request.user.role == 'ADAY':
            return self.queryset.filter(tablo5__basvuru__aday=self.request.user)
        elif self.request.user.role in ['ADMIN', 'YONETICI']:
            return self.queryset.all()
        elif self.request.user.role == 'JURI_UYESI':
            return self.queryset.filter(tablo5__basvuru__status='SUBMITTED')
        return self.queryset.none()