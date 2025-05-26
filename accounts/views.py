from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
# Create your views here.

class UserListCreate(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Set user as active when created
            user.is_active = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Manually set the backend attribute for the login function
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            # Create or get token for authentication
            token, created = Token.objects.get_or_create(user=user)
            
            # Return user data and token
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'full_name': user.full_name,
                'is_premium': user.is_premium,
                'role' : user.role,
                'credits': user.credits
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)