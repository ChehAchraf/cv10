from django.urls import path
from .views import UserListCreate, UserLogin

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('login/', UserLogin.as_view(), name='user-login'),
]
