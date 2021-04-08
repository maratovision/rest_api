from rest_framework import views, status
from rest_framework.response import Response

from .serializers import *


class RegisterView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user= request.user)
        except TypeError:
            return Response({"data": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except TypeError:
            return Response({"data": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CardCreateSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.data.get('number')
            holder = serializer.data.get('holder_name')
            date = serializer.data.get('date')
            code = serializer.data.get('code')
            Cards.objects.create(profile= profile, number= number, holder_name= holder, date= date, code= code)
            return Response({'CARD ADDED SUCCESS!'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors)
