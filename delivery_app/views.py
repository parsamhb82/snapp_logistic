from django.http.response import HttpResponse, JsonResponse
from delivery_app.models import Delivery, Courier, Location
from django.shortcuts import render

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
def add_delivery(request, code, origin_lat, origin_long, destination_lat, destination_long, courier_id):
    courier = Courier.objects.get(id = courier_id)
    origin = Location.objects.create(lat = origin_lat, long = origin_long)
    destination = Location.objects.create(lat = destination_lat, long = destination_long)
    delivery = Delivery.objects.create(code = code, origin = origin, destination = destination, courier = courier, courier_phone_number = courier.courier_phone_number, courier_plate = courier.plate)
    delivery.save()
    return HttpResponse(f"delivery with code {delivery.code} created successfully")

def check_delivery_status(request, code):
    delivery = Delivery.objects.get(code = code)
    return HttpResponse(f"delivery with code {delivery.code} is {delivery.delivery_status}")

def cancle_delivery(request, code):
    delivery = Delivery.objects.get(code = code)
    delivery.delivery_status = 10
    delivery.save() 
    return HttpResponse(f"delivery with code {delivery.code} is cancled")