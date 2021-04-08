from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import *
from django.contrib.auth.models import User



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=16)
    confirm_password = serializers.CharField(write_only=True, min_length=8, max_length=16)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError({'data': 'password dont match'})
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user= user, email= user.email,
                                   full_name= user.first_name.capitalize() + ' ' + user.last_name.capitalize())
        return user


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cards
        fields = '__all__'


class CardCreateSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    date = serializers.DateField()
    holder_name = serializers.CharField(max_length=20)
    code = serializers.IntegerField(min_value=100, max_value=999)


class UserProfileSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True)
    bonuses = serializers.IntegerField(read_only=True)
    order_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'full_name', 'phone', 'email', 'street', 'house', 'bonuses', 'order_count', 'cards']
