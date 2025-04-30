from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role == 'ADMIN'

class IsYonetici(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role == 'YONETICI'

class IsJuriUyesi(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role == 'JURI_UYESI'

class IsAday(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role == 'ADAY'

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        # Nesnenin sahibi veya admin/yönetici ise izin ver
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.role in ['ADMIN', 'YONETICI']
        return obj == request.user or request.user.role in ['ADMIN', 'YONETICI']

class IsAdminOrYonetici(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in ['ADMIN', 'YONETICI'] 