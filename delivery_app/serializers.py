from .models import Delivery, Courier, Wallet, Transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class DeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class DeliveryStatusSerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['code', 'delivery_status']
    

class CreateDeliverySerializer(serializers.Serializer):
    origin_lat = serializers.FloatField()
    origin_long = serializers.FloatField()
    destination_lat = serializers.FloatField()
    destination_long = serializers.FloatField()


class CourierSerializer(ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class CourierRegisterSerializer(ModelSerializer):
    plate = serializers.CharField(max_length=10)
    courier_phone_number = serializers.CharField(max_length=11)
    

    class Meta:
        model = User
        fields = ['username', 'password', 'plate', 'courier_phone_number', 'first_name', 'last_name']