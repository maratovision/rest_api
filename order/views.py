from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from rest_framework import views, status
from .servises import salary_increase, worker_count_order
from django.utils import timezone


class OrderView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # # count_orders(user)
            order_id = serializer.data.get('id')
            try:
                profile = EmployeeProfile.objects.get(user= request.user)
            except EmployeeProfile.DoesNotExist:
                profile = UserProfile.objects.get(user= request.user)
            if isinstance(profile, EmployeeProfile):
                order = Order.objects.get(id= order_id)
                order.worker = request.user.employeeprofile
                order.save()
            # total_sum = serializer.data.get('total_sum')
            # # get_pay(order_id)
            # # count_bonuses(user, total_sum)
            return Response({'data': 'OK'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class TableView(views.APIView):

    def get(self, request, *args, **kwargs):
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': 'OK'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class TableDetailView(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            table = Table.objects.get(area=kwargs['table_area'])
        except Table.DoesNotExist:
            return Response({'data': 'Table not found'}, status.HTTP_404_NOT_FOUND)
        serializer = TableDetailSerializer(table)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TableDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': 'OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class EmployeeView(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            worker = EmployeeProfile.objects.get(user= request.user)
        except EmployeeProfile.DoesNotExist:
            return Response({'data':'not worker'})
        worker_count_order(worker)
        salary_increase(worker)
        serializer = EmployeeSerializer(worker)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = EmployeeProfile.objects.get(user= request.user)
        serializer = EmployeeSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': 'updates success'})
        return Response(serializer.errors)


class ModifyOrderView(views.APIView):

    def put(self, request, *args, **kwargs):
        order = Order.objects.get(id= kwargs['order_id'])
        order_minute, order_hour = order.date_created.minute, order.date_created.hour * 60
        current_minute, current_hour = timezone.now().minute, timezone.now().hour * 60
        order_time = order_minute + order_hour
        current_time = current_minute + current_hour
        abs_value = abs(order_time - current_time)
        serializer = OrderSerializer(order, data= request.data)
        if serializer.is_valid():
            if abs_value <= 5 and order.status == 'in process':
                serializer.save()
                # order_id = serializer.data.get('id') my homework
                # count_order(order_id)
                return Response({'data': 'order updated success'})
            return Response({'data': f'time is up or order is {order.status}'})
        return Response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['order_id'])
        order_minute, order_hour = order.date_created.minute, order.date_created.hour * 60
        current_minute, current_hour = timezone.now().minute, timezone.now().hour * 60
        order_time = order_minute + order_hour
        current_time = current_minute + current_hour
        abs_value = abs(order_time - current_time)
        if abs_value <= 5 and order.status == 'in process':
            order.delete()
            return Response({'data': 'order is canceled'})
        return Response({'data': f'time is up or order is {order.status}'})


class AdminUserPutOrder(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id= kwargs['order_id'], status__in=['in process', 'ready'])
        except Order.DoesNotExist:
            return Response(f'Order not found or order closed', status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        order = Order.objects.get(id= kwargs['order_id'], status__in=['in process', 'ready'])
        serializer = CloseOrderSerializer(data= request.data)
        if serializer.is_valid():
            guest_money = serializer.data.get('guest_money')
            if guest_money >= order.total_price:
                change = guest_money - order.total_price
                order.status = serializer.data.get('new_status')
                order.save()
                return Response(f'Ваша сдача: {change}', status=status.HTTP_200_OK)
            return Response({'data': 'Not enough money'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
