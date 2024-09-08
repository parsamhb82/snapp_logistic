from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from delivery_app.models import Delivery, Courier, Location, Wallet
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import random
import requests
from .serializers import DeliverySerializer, DeliveryStatusSerializer, CreateDeliverySerializer, CourierRegisterSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
import uuid
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from .permissions import CourierPermission, SuperUserPermission
from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CourierLoginView(TokenObtainPairView):
    pass

class CourierRefreshView(TokenRefreshView):
    pass

def API_to_find_all_deliveries(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        courier_lat = data['courier_lat']
        courier_long = data['courier_long']
        deliveries = Delivery.objects.filter(delivery_status = 1)
        paramsstr = ''
        for delivery in deliveries :
            paramsstr += f"{delivery.origin.lat},{delivery.origin.long}|"
        paramsstr = paramsstr[:-1]
        url = f"https://api.neshan.org/v1/distance-matrix/no-traffic?type=car&origins={courier_lat},{courier_long}&destinations={paramsstr}"
        api_key = 'service.9fc8ab4077f34c9eaf03966f572c33f6'
        response = requests.get(url, headers={'Api-Key': api_key})
        json_file = json.loads(response.content)
        return json_file

            

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['price', 'max_delivery_time']


class ShowAvailableDelivery(ListAPIView):
    queryset = Delivery.objects.filter(delivery_status = 1)
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, CourierPermission]
    




def api_to_neshan(orilat, orilong, destlat,destlong):
    
    url = f'https://api.neshan.org/v4/direction?type=motorcycle&origin={orilat},{orilong}&destination={destlat},{destlong}'
    api_key = 'service.9fc8ab4077f34c9eaf03966f572c33f6'
    response = requests.get(url, headers={'Api-Key': api_key})
    json_file = json.loads(response.content)
    #distance = json_file["routes"][0]['legs'][0]['distance']['value']
    return json_file
    
class CreateDelivery(APIView):

    def post(self, request):
        serializer = CreateDeliverySerializer(data = request.data)
        if serializer.is_valid():
            code = generate_unique_delivary_code()
            origin = Location.objects.create(lat = serializer.validated_data['origin_lat'], long = serializer.validated_data['origin_long'])
            destination = Location.objects.create(lat = serializer.validated_data['destination_lat'], long = serializer.validated_data['destination_long'])
            json_file = api_to_neshan(serializer.validated_data['origin_lat'], serializer.validated_data['origin_long'], serializer.validated_data['destination_lat'], serializer.validated_data['destination_long'])
            delivery_price = json_file["routes"][0]['legs'][0]['distance']['value']
            delivary_duration = json_file["routes"][0]['legs'][0]['duration']['value']
            delivary_duration = int(delivary_duration) + random.randint(100, 1000)
            delivary_duration = delivary_duration = (delivary_duration // 60) + 1
            delivery_price = int(delivery_price) * 10
            delivery = Delivery.objects.create(code = code, origin = origin, destination = destination, delivery_status = 1, max_delivery_time = f'{delivary_duration}', delivery_price = delivery_price, courier = None)
            return Response({"message": "Delivery created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
    
class ShowDeliveriesToCourier(APIView):
    permission_classes = [IsAuthenticated, CourierPermission]

    def get(self, request):
        deliveries = Delivery.objects.filter(delivery_status = 1)
        courier_lat = 35.725729
        courier_long = 51.373739
        lats = []
        longs = []
        paramsstr = ''
        for delivery in deliveries:
            if delivery.status == 1:
                paramsstr += f"{delivery.origin.lat},{delivery.origin.long}|"
        paramsstr = paramsstr[:-1]
        url = f"https://api.neshan.org/v1/distance-matrix/no-traffic?type=car&origins={courier_lat},{courier_long}&destinations={paramsstr}"
        api_key = 'service.680950bb710e40c59ec4c81b22f131c4'
        response = requests.get(url, headers={'Api-Key': api_key})
        json_file = json.loads(response.content)
        if json_file['status'] == 'OK':
            rows = json_file['rows'][0]
            elements = rows['elements']
            response_data = []
            for element in elements:
                if element['status'] == 'OK':
                    distance = element['distance']['value']
                    if distance <= 3000:
                        response_data.append(element)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": "Bad request Couldn't get the info from neshan"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateDelivery(UpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, CourierPermission]

    def update(self, request, *args, **kwargs):
        delivery = self.get_object()
        if delivery.delivery_status == 1:
            delivery.delivery_status = 2
            delivery.courier = request.user.courier
            delivery.save()
            return Response({"message": "Delivery updated successfully"}, status=status.HTTP_200_OK)
        elif delivery.delivery_status == 2:
            courier = request.user.courier
            courier.wallet.current_money += delivery.delivery_price
            delivery.delivery_status = 3
        return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class CourierRegistrationView(CreateAPIView):
    serializer_class = CourierRegisterSerializer

    def perform_create(self, serializer):
        user = User.objects.create_user(username=serializer.validated_data['username'], 
                                        password=serializer.validated_data['password'], 
                                        first_name=serializer.validated_data['first_name'], 
                                        last_name=serializer.validated_data['last_name'],
                                        natinal_code=serializer.validated_data['natinal_code'])
        courier = Courier.objects.create(user=user, courier_phone_number = serializer.validated_data['courier_phone_number'], plate=serializer.validated_data['plate'])
        wallet = Wallet.objects.create(user=user, current_money = 0)





            



        