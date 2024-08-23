from django.http.response import HttpResponse, JsonResponse
from delivery_app.models import Delivery, Courier, Location
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import random

def show_delivery(request):
    deliveries = Delivery.objects.all()
    deliveries_list = []
    for item in deliveries:
        delivery_dict = {
            "code" : item.code,
            "origin" : item.origin.lat,
            "destination" : item.origin.long

        } 
        deliveries_list.append(delivery_dict)
        return JsonResponse(deliveries_list, safe=False)

def welcome_page(request):
    return render(request, 'delivery_app/welcome.html')
@csrf_exempt
def add_delivery(request):
    if request.method == 'POST':
        while(True):
            code = random.randint(1, 9999999)
            try :
                this_delivery = Delivery.objects.get(code = code)

            except:
                break
        body = json.loads(request.body)
        origin = Location.objects.create(lat = body['origin_lat'], long = body['origin_long'])
        destination = Location.objects.create(lat = body['destination_lat'], long = body['destination_long'])
        delivery = Delivery.objects.create(code = code, origin = origin, destination = destination, delivery_status = 1, max_delivery_time = '1', delivery_price = '1', courier = None)
        delivery.save()
        return HttpResponse(f"delivery with code {delivery.code} created successfully")
    else:
        return HttpResponse('bad request')

def check_delivery_status(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            delivery = Delivery.objects.get(code = body['code'])
            return JsonResponse({"status" : delivery.delivery_status})
        except:
            return HttpResponse('bad request')
    else:
        return HttpResponse('bad request')
    

def cancle_delivery(request, code):
    if request.method == 'POST':
         delivery = Delivery.objects.get(code = code)
         delivery.delivery_status = 10
         delivery.save() 
         return HttpResponse(f"delivery with code {delivery.code} is cancled")
    else:
        return HttpResponse('bad request')
def choose_delivery(request):
    pass