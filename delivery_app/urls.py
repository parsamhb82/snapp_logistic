from django.urls import path
from delivery_app.views import welcome_page, add_delivery

urlpatterns = [
    path('', welcome_page),
    path('add_delivery/<str:code>/<str:origin_lat>/<str:origin_long>/<str:destination_lat>/<str:destination_long>/<int:courier_id>', add_delivery)
]