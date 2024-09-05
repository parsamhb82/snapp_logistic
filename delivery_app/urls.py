from django.urls import path
from delivery_app.views import welcome_page, add_delivery, cancle_delivery, DeliveryList

urlpatterns = [
    path('', welcome_page),
    path('add_delivery/<str:code>/<str:origin_lat>/<str:origin_long>/<str:destination_lat>/<str:destination_long>/<int:courier_id>/', add_delivery),
    #path('check_delivery_status/<str:code>/', check_delivery_status),
    path('cancle_delivery/<str:code>/', cancle_delivery),
    path('delivey_list/', DeliveryList.as_view()),
    #path('find_distance/<str:orilat>/<str:orilong>/<str:destlat>/<str:destlong>/', find_distance)
]