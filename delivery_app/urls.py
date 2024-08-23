from django.urls import path
from delivery_app.views import welcome_page

urlpatterns = [
    path('', welcome_page)
]