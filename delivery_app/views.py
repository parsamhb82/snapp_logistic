from django.http.response import HttpResponse, JsonResponse
from delivery_app.models import Delivery, Courier, Location
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import random
import requests
from .serializers import DeliverySerializer, DeliveryStatusSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
import uuid
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from .permissions import CourierPermission, SuperUserPermission


class CourierLoginView(TokenObtainPairView):
    pass

class CourierRefreshView(TokenRefreshView):
    pass

def generate_unique_delivary_code():
    while True:
        code = str(uuid.uuid4())[:16]
        if not Delivery.objects.filter(code = code).exists():
            return code


class DeliveryList(ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [SuperUserPermission]

def welcome_page(request):
    return render(request, 'delivery_app/welcome.html')


@csrf_exempt
def add_delivery(request):
    if request.method == 'POST':
        code = generate_unique_delivary_code()
        body = json.loads(request.body)
        origin = Location.objects.create(lat = body['origin_lat'], long = body['origin_long'])
        destination = Location.objects.create(lat = body['destination_lat'], long = body['destination_long'])
        json_file = api_to_neshan(body['origin_lat'], body['origin_long'], body['destination_lat'], body['destination_long'])
        delivery_price = json_file["routes"][0]['legs'][0]['distance']['value']
        delivary_duration = json_file["routes"][0]['legs'][0]['duration']['value'] 
        delivary_duration = int(delivary_duration) + random.randint(100, 1000)
        delivary_duration = (delivary_duration // 60) + 1
        delivery_price = int(delivery_price) * 10
        delivery = Delivery.objects.create(code = code, origin = origin, destination = destination, delivery_status = 1, max_delivery_time = f'{delivary_duration}', delivery_price = delivery_price, courier = None)
        delivery.save()
        return HttpResponse(f"delivery with code {delivery.code} created successfully")
    else:
        return HttpResponse('bad request')
    
class RetrieveDeliverystatus(RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated, CourierPermission]
  

def cancle_delivery(request, code):
    if request.method == 'POST':
         delivery = Delivery.objects.get(code = code)
         delivery.delivery_status = 10
         delivery.save() 
         return HttpResponse(f"delivery with code {delivery.code} is cancled")
    else:
        return HttpResponse('bad request')


class ChooseDelivery(ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, CourierPermission]

class ShowAvailableDelivery(ListAPIView):
    queryset = Delivery.objects.filter(delivery_status = 1).order_by('delivery_price')
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, CourierPermission]
    




def api_to_neshan(request, orilat, orilong, destlat,destlong):
    
    url = f'https://api.neshan.org/v4/direction?type=motorcycle&origin={orilat},{orilong}&destination={destlat},{destlong}'
    api_key = 'service.9fc8ab4077f34c9eaf03966f572c33f6'
    response = requests.get(url, headers={'Api-Key': api_key})
    json_file = json.loads(response.content)
    #distance = json_file["routes"][0]['legs'][0]['distance']['value']
    return json_file
    