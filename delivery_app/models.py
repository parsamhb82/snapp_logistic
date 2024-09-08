from django.db import models
from django.contrib.auth.models import User

class Courier(models.Model):
    user = models.OneToOneField(User, on_delete = models.PROTECT, blank=True, null=True)
    courier_status = models.IntegerField()
    plate = models.CharField(max_length=8)
    courier_phone_number = models.CharField(max_length=11)
    def __str__(self) -> str:
        return self.user.username


class Location(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    def __str__(self) -> str:
        return f"{self.lat}, {self.long}"


class Delivery(models.Model):
    code = models.CharField(max_length = 16, unique=True)
    origin = models.ForeignKey(Location, on_delete = models.CASCADE, related_name='delivery_origin')  
    destination = models.ForeignKey(Location, on_delete = models.CASCADE, related_name='delivery_destiation')  
    courier = models.ForeignKey(Courier, on_delete = models.PROTECT, blank = True, null = True)
    delivery_status = models.IntegerField()
    max_delivery_time = models.CharField(max_length=120)
    delivery_price = models.FloatField()
    def __str__(self) -> str:
        return self.code
    class Meta:
        verbose_name = "delivery"
        verbose_name_plural = "deliveries" 

class Wallet(models.Model):
    current_money = models.IntegerField(blank = True, null = True)
    courier = models.OneToOneField(Courier, on_delete = models.CASCADE, blank = True, null = True)


    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank = True, null=True)
    amount = models.FloatField(blank=True, null=True)
    


    



    

