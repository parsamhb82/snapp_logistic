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
