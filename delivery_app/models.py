from django.db import models

class Courier(models.Model):
    name = models.CharField(max_length = 50, help_text="the courior name should have less than 50 characters")
    wallet = models.OneToOneField('Wallet', on_delete = models.PROTECT)
    courier_status = models.IntegerField()
    plate = models.CharField(max_length=8)
    courier_phone_number = models.CharField(max_length=11)
    def __str__(self) -> str:
        return self.name


class Location(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    def __str__(self) -> str:
        return f"{self.lat}, {self.long}"


class Delivery(models.Model):
    code = models.CharField(max_length = 7, unique=True)
    origin = models.ForeignKey(Location, on_delete = models.CASCADE, related_name='delivery_origin', verbose_name="delivery_code")  
    destination = models.ForeignKey(Location, on_delete = models.CASCADE, related_name='delivery_destiation', verbose_name="customer_addres")  
    courier = models.ForeignKey(Courier, on_delete = models.PROTECT, blank = True, null = True)
    delivery_status = models.IntegerField()
    max_delivery_time = models.CharField(max_length=120)
    delivery_price = models.FloatField()
    def __str__(self) -> str:
        return self.code
    class Meta:
        verbose_name = "my_delivery"
        verbose_name_plural = "my_delivery" 

class Wallet(models.Model):
    current_money = models.IntegerField(blank = True, null = True)

    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank = True, null=True)
    


    



    

