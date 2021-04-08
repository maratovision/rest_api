from rest_framework.permissions import IsAuthenticated
from order.serializers import EmployeeSerializer
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from order.models import Order
from order.serializers import OrderSerializer


class RateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args , **kwargs):
        try:
            profile = UserProfile.objects.get(user= request.user)
        except UserProfile.DoesNotExist:
            try:
                profile = EmployeeProfile.objects.get(user= request.user)
            except EmployeeProfile.DoesNotExist:
                return Response({'data': 'Please log in!'})

        if isinstance(profile, UserProfile):
            orders = Order.objects.filter(user_profile=profile)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        return Response({'data': 'this is not for you'})


class RateWorkerView(APIView):

    def get(self, request, *args, **kwargs):
        worker = EmployeeProfile.objects.get(id= kwargs['worker_id'])
        serializer = EmployeeSerializer(worker)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RateCreateSerializer(data= request.data)
        worker = EmployeeProfile.objects.get(id= kwargs['worker_id'])
        userprofile = request.user.userprofile
        if serializer.is_valid():
            Rate.objects.create(star= serializer.data.get('star'), worker= worker, profile= userprofile)
            return Response({'data': 'Okay!'})
        else:
            return Response(serializer.errors)
