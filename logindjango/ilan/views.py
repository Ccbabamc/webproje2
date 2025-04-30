from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Fakulte, Bolum, Kriter, Ilan
from .serializers import (
    FakulteSerializer,
    BolumSerializer,
    KriterSerializer,
    IlanListSerializer,
    IlanDetailSerializer,
    IlanCreateUpdateSerializer,
    IlanSerializer,
    FrontendIlanCreateSerializer,
)
# Import necessary permissions
from users.permissions import IsAdmin, IsYonetici, IsJuriUyesi, IsAday, IsAdminOrYonetici 
# Removed IsSuperUser import as it doesn't exist in users.permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser # Import standard permissions

# Create your views here.

class FakulteViewSet(viewsets.ModelViewSet):
    queryset = Fakulte.objects.all()
    serializer_class = FakulteSerializer
    # Default permission can be IsAuthenticated, specific actions will override
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ad']
    ordering_fields = ['ad', 'created_at']

    def get_permissions(self):
        """
        Set permissions based on action.
        Allow any authenticated user to list/retrieve.
        Restrict create/update/delete to Admin/Yonetici/Superuser.
        """
        # Explicitly allow any authenticated user for list and retrieve
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated] 
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only allow Admin, Yonetici, or Superuser to modify
            permission_classes = [IsAdminOrYonetici] 
        else:
            # Default deny for other actions if any
            permission_classes = [permissions.IsAdminUser] 
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        # Ensure permission check happens correctly before list execution
        # The permission check is handled by DRF before calling this method
        queryset = self.filter_queryset(self.get_queryset())
        
        # Frontend uyumluluğu için veriyi özelleştir
        faculties = [{
            'id': faculty.id,
            'name': faculty.ad
        } for faculty in queryset]
        
        return Response(faculties)

class BolumViewSet(viewsets.ModelViewSet):
    queryset = Bolum.objects.all()
    serializer_class = BolumSerializer
    permission_classes = [permissions.IsAuthenticated] # Default permission
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['ad', 'fakulte__ad']
    filterset_fields = ['fakulte']
    ordering_fields = ['ad', 'fakulte__ad', 'created_at']

    def get_permissions(self):
        """
        Set permissions based on action.
        Allow any authenticated user to list/retrieve.
        Restrict create/update/delete to Admin/Yonetici/Superuser.
        """
        if self.action in ['list', 'retrieve']:
             # Allow any authenticated user to view departments
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
             # Only allow Admin, Yonetici, or Superuser to modify
            permission_classes = [IsAdminOrYonetici] 
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Fakulte ID'sini farklı parametre isimlerinden alabilmek için kontrol
        faculty_id = None
        
        # Önce standart Django Rest Framework filterset params
        if 'fakulte' in request.query_params:
            faculty_id = request.query_params.get('fakulte')
        
        # Frontend uyumluluğu için faculty_id parametresini de kontrol et
        elif 'faculty_id' in request.query_params:
            faculty_id = request.query_params.get('faculty_id')
        
        # Ayrıca faculty parametre ismini de kontrol et
        elif 'faculty' in request.query_params:
            faculty_id = request.query_params.get('faculty')
            
        # Fakülte ID'sine göre filtrele
        if faculty_id:
            # Debug için konsola yazdır
            # print(f"Filtering departments by faculty_id: {faculty_id}") # Removed debug log
            queryset = queryset.filter(fakulte_id=faculty_id)
        
        # Diğer filtreleri uygula (search, ordering etc.)
        # Note: filter_queryset should ideally be called after initial filtering
        # queryset = self.filter_queryset(queryset) # Let's apply DRF filters later if needed

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
             # Frontend uyumluluğu için veriyi özelleştir
            departments = [{
                'id': department.id,
                'name': department.ad,
                'faculty': department.fakulte_id if department.fakulte else None
            } for department in page]
            return self.get_paginated_response(departments)

        # No pagination case (should ideally not happen with default settings)
        departments = [{
            'id': department.id,
            'name': department.ad,
            'faculty': department.fakulte_id if department.fakulte else None
        } for department in queryset]
        return Response(departments)


class KriterViewSet(viewsets.ModelViewSet):
    queryset = Kriter.objects.all()
    serializer_class = KriterSerializer
    permission_classes = [permissions.IsAuthenticated] # Default permission

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrYonetici]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class IlanViewSet(viewsets.ModelViewSet):
    queryset = Ilan.objects.select_related('bolum', 'bolum__fakulte').prefetch_related('kriterler').all() # Optimized query
    serializer_class = IlanSerializer # Default serializer
    permission_classes = [permissions.IsAuthenticated] # Base permission
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] # Add SearchFilter and OrderingFilter
    filterset_fields = ['bolum', 'status', 'bolum__fakulte'] # Allow filtering by faculty via department
    search_fields = ['baslik', 'aciklama', 'bolum__ad', 'bolum__fakulte__ad'] # Fields to search in
    ordering_fields = ['created_at', 'son_basvuru_tarihi', 'baslik'] # Fields allowed for ordering
    ordering = ['-created_at'] # Default ordering

    def get_permissions(self):
        """
        Set permissions based on action.
        Allow authenticated users to list/retrieve.
        Restrict create/update/delete to Admin/Yonetici/Superuser.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrYonetici]
        else:
             permission_classes = [permissions.IsAdminUser] # Default deny
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return IlanListSerializer
        elif self.action == 'retrieve':
            return IlanDetailSerializer
        # Use the same serializer for create/update for simplicity unless frontend sends different structure
        elif self.action in ['create', 'update', 'partial_update']:
             # Check if frontend-specific fields are present
             # This check might be fragile, consider a dedicated endpoint or header if possible
            # if self.request.data and ('title' in self.request.data or 'department' in self.request.data):
            #     return FrontendIlanCreateSerializer 
            return IlanCreateUpdateSerializer # Use the standard create/update serializer
        return IlanSerializer # Default

    # create method override removed as standard ModelViewSet create should work with correct serializer

    # list method override removed, default pagination and serialization should work

    def get_queryset(self):
        """
        Filter queryset based on user role.
        """
        # Return empty queryset for swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
        
        # Superuser and Admin/Yonetici see all ilanlar
        if user.is_superuser or (hasattr(user, 'role') and user.role in ['ADMIN', 'YONETICI']):
            return self.queryset.all()
        # Juri members see ilanlar they are assigned to (assuming a relation exists)
        # elif hasattr(user, 'role') and user.role == 'JURI_UYESI':
            # Add filtering based on jury assignment if applicable
            # return self.queryset.filter(juri_uyeleri=user) # Example filter
        # Aday users see only AKTIF ilanlar
        elif hasattr(user, 'role') and user.role == 'ADAY':
            return self.queryset.filter(status=Ilan.Status.AKTIF)
        
        # Default deny for other roles or users without roles
        return self.queryset.none()
