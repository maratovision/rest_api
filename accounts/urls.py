from django.urls import path
from .views import *

urlpatterns = [
    path('userprofile/', UserProfileView.as_view()),
    path('register/', RegisterView.as_view(), name= 'create')
]