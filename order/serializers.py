from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from accounts.servises import *


class MTOSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = MealToOrder
        fields = ['id', 'meal', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    total_price = serializers.IntegerField(min_value=0, read_only=True)
    total_sum = serializers.SerializerMethodField()
    MTO = MTOSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'table', 'status', 'date_created','user_profile', 'total_sum', 'worker', 'MTO']

    def create(self, validated_data):
        mto_data = validated_data.pop('MTO')
        order = Order.objects.create(**validated_data)

        for mto in mto_data:
            drop_id = mto.pop('id')
            MealToOrder.objects.create(order=order, **mto)
        return order

    def update(self, instance, validated_data):
        instance.table = validated_data.get('table', instance.table)
        instance.save()
        mto_data = validated_data.get('MTO')
        for mto in mto_data:
            mto_instance = MealToOrder.objects.get(id=mto.get('id'))
            mto_instance.meal = mto.get('meal', mto_instance.meal)
            mto_instance.quantity = mto.get('quantity', mto_instance.quantity)
            mto_instance.save()
        return instance

    def get_total_sum(self, obj):
        total_sum = 0
        for mto in obj.MTO.all():
            total_sum += mto.meal.price * mto.quantity
        obj.total_price = total_sum
        obj.save()
        return total_sum


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ['id', 'area', 'status']


class TableDetailSerializer(serializers.ModelSerializer):
    order_set = OrderSerializer(many=True)

    class Meta:
        model = Table
        fields = ['id', 'area', 'status', 'order_set']

    def create(self, validated_data):
        order_data = validated_data.pop('order_set')
        table = Table.objects.create(**validated_data)
        for order in order_data:
            Order.objects.create(table=table, **order)
        return table


class EmployeeSerializer(serializers.ModelSerializer):
    salary = serializers.IntegerField(read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = '__all__'


class CloseOrderSerializer(serializers.Serializer):
    new_status = serializers.ChoiceField(choices=(('closed', 'closed')))
    guest_money = serializers.IntegerField(min_value=0)
