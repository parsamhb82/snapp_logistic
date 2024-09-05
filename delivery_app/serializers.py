from .models import Delivery
from rest_framework.serializers import ModelSerializer

class DeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

class DeliveryStatusSerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['code', 'delivery_status']