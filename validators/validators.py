from users.models import User
from rest_framework import serializers

def username_validation(username):
    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError(
            {
                'error': f'User with username: {username} exists.'
            }
        )
        

def email_validation(email):
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError(
            {
                'error'f'User with email: {email} exists.'
            }
        )

def password_validation(password, password2):
    if password != password2:
        raise serializers.ValidationError({'error': "Passwords don't match"})