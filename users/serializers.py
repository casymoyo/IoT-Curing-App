from . models import User
from rest_framework import serializers
from validators.validators import (
    username_validation,
    email_validation,
    password_validation
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
            'username', 
            'email',
            'role'
            'password', 
            'password2',
        ]
    
    extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        username  = attrs.get('username')
        
        email_validation(email)
        username_validation(username)
        password_validation(password, password2)
        
        return attrs
    
    def create(self, validated_data):
        User.object.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data['role']
        )
