from .models import User
from loguru import logger
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import (
    UserSerializer,
    UserRegisterSerializer
)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer  

    def get_queryset(self):
        return super().get_queryset()

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]  
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = UserRegisterSerializer(user, context=self.get_serializer_context()).data
        token = Token.objects.get(user=user).key
        
        return Response(
            {
                'user': user_data,
                'token': token,
                'message': 'Account created successfully'
            }
        )

class CustomAuthToken(ObtainAuthToken):
   
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['username']
        
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=403)

        token, created = Token.objects.get_or_create(user=user)
        
        logger.info(User.objects.get(username = user))
        
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user).data
            }
        )

        