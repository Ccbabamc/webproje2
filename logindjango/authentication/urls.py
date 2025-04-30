from django.urls import path
from .views import TCObtainAuthToken

urlpatterns = [
    path('login/', TCObtainAuthToken.as_view(), name='tc-auth-token'),
] 