from django.http.response import HttpResponse, JsonResponse
from delivery_app.models import Delivery, Courier, Location

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
        
