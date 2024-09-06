from .models import Delivery
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

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