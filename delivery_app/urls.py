from django.urls import path
from delivery_app.views import (welcome_page,
                                cancle_delivery,
                                DeliveryList,
                                CreateDelivery,
                                ShowDeliveriesToCourier,
                                CourierLoginView,
                                CourierRefreshView,
                                RetrieveDeliverystatus,
                                ChooseDelivery,
                                ShowAvailableDelivery,
                                UpdateDelivery,
                                CourierRegistrationView)


urlpatterns = [
    path('', welcome_page),
    path('cancle_delivery/<str:code>/', cancle_delivery),
    path('delivey_list/', DeliveryList.as_view()),
    path('create_delivery/', CreateDelivery.as_view()),
    path('show_deliveries_to_courier/', ShowDeliveriesToCourier.as_view()),
    path('courier-login/', CourierLoginView.as_view()),
    path('courier-refresh/', CourierRefreshView.as_view()),
    path('retrieve-delivery-status/', RetrieveDeliverystatus.as_view()),
    path('choose-delivery/', ChooseDelivery.as_view()),
    #path('show-available-delivery/', ShowAvailableDelivery.as_view()),
    path('update-delivery/', UpdateDelivery.as_view()),
    path('courier-registration/', CourierRegistrationView.as_view())
]