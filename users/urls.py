from django.urls import path
from .views import CustomAuthToken, UserRegistrationView, UserListView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', CustomAuthToken.as_view(), name='token'),
    path('users/', UserListView.as_view(), name='user-list'),
]
