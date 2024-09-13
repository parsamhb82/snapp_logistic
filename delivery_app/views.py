from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from delivery_app.models import Delivery, Courier, Location, Wallet, Transaction
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
import environ
env = environ.Env()
environ.Env.read_env()


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

    
class RetrieveDeliverystatus(RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated, CourierPermission]

    def get_queryset(self):
        return Delivery.objects.filter(courier = self.request.user.courier)
  

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
    api_key = env('API_KEY')
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
            delivery_summary = json_file["routes"][0]['legs'][0]['summary']
            delivery = Delivery.objects.create(code = code, origin = origin, destination = destination, delivery_status = 1, max_delivery_time = f'{delivary_duration}', delivery_price = delivery_price, courier = None, summary = delivery_summary)
            return Response({"message": "Delivery created successfully",
                             "delivary_price" : delivery_price}, status=status.HTTP_201_CREATED)
        return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
    
class ShowDeliveriesToCourier(APIView):
    permission_classes = [IsAuthenticated, CourierPermission]

    def post(self, request):
        if request.user.courier.courier_status == 2:
            return Response({"error": "You are not available"}, status=status.HTTP_400_BAD_REQUEST)
        deliveries = Delivery.objects.filter(delivery_status = 1)
        courier_lat = request.data['lat']
        courier_long = request.data['long']
        paramsstr = ''
        lats = []
        longs = []
        for delivery in deliveries:
            if delivery.delivery_status == 1:
                paramsstr += f"{delivery.origin.lat},{delivery.origin.long}%7C"
                lats.append(delivery.origin.lat)
                longs.append(delivery.origin.long)

        paramsstr = paramsstr[:-3]
        url = f"https://api.neshan.org/v1/distance-matrix?type=motorcycle&origins={courier_lat},{courier_long}&destinations={paramsstr}"
        api_key = env("API_KEY_NESHAN_ADJACENT_MATRIX")
        response = requests.get(url, headers={'Api-Key': api_key})
        json_file = json.loads(response.content)
        if json_file['status'] == 'Ok':
            destinations = json_file['destination_addresses']   
            rows = json_file['rows'][0]
            elements = rows['elements']
            response_data = []
            for count, element in enumerate(elements):
                if element['status'] == 'Ok':
                    distance = element['distance']['value']
                    if distance <= 100000000000:
                        response_data.append(
                            {
                                'delivery_code': deliveries[count].code,
                                'delivery_price': deliveries[count].delivery_price,
                                'delivery_origin_lat': deliveries[count].origin.lat,
                                'delivery_origin_long': deliveries[count].origin.long,
                                'delivery_destination_lat': deliveries[count].destination.lat,
                                'delivery_destination_long': deliveries[count].destination.long,
                                'delivery_max_delivery_time': deliveries[count].max_delivery_time,
                                'delivery_distance': distance,
                                'delivery_destination_address': destinations[count],
                                'delivery_summary' : deliveries[count].summary
                            }
                        )
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": "Bad request Couldn't get the info from neshan"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateDelivery(UpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, CourierPermission]


    def update(self, request, *args, **kwargs):
        delivery = self.get_object()
        if request.user != delivery.courier:
            return Response({"error": "You are not the courier of this delivery"}, status=status.HTTP_400_BAD_REQUEST)
        if delivery.delivery_status == 1 and delivery.courier == None and request.user.courier.courier_status == 1:
            delivery.delivery_status = 2
            delivery.courier = request.user.courier
            courier = request.user.courier
            courier.courier_status = 2
            delivery.save()
            courier.save()
            return Response({"message": "Delivery updated successfully"}, status=status.HTTP_200_OK)
        elif delivery.delivery_status == 2  and delivery.courier == request.user.courier:
            courier = request.user.courier
            transaction = Transaction.objects.create(wallet = courier.wallet, amount = delivery.delivery_price)
            courier.wallet.amount += delivery.delivery_price
            delivery.delivery_status = 3
            courier.courier_status = 1
            delivery.save()
            courier.save()
            return Response({"message": "Delivery updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class CourierRegistrationView(CreateAPIView):
    serializer_class = CourierRegisterSerializer

    def perform_create(self, serializer):
        user = User.objects.create_user(username=serializer.validated_data['username'], 
                                        password=serializer.validated_data['password'], 
                                        first_name=serializer.validated_data['first_name'], 
                                        last_name=serializer.validated_data['last_name'])
        courier = Courier.objects.create(user=user, courier_phone_number = serializer.validated_data['courier_phone_number'], plate=serializer.validated_data['plate'], courier_status = 1)
        wallet = Wallet.objects.create(courier=courier, current_money = 0)        