from django.db import models

category_ch=(("speedbreaker","speedbreaker"),("normal","normal"),("rough_surface","rough_surface"),("Descend","Descend"),("ascend","ascend"),("obstacle","obstacle"))
env_ch=(("rainy","rainy"),("foggy","foggy"),("Sunny","Sunny"),("cloudy","cloudy"),("Snow","Snow"),("night","night"),("forest","forest"))

class Vehicle(models.Model):
    vehicle_name=models.CharField(max_length=128)
    is_active=models.BooleanField(default=False)

    def __Str__(self):
        return f'{self.vehicle_name}'

class Location(models.Model):
    place=models.CharField(max_length=128)
    is_active=models.BooleanField(default=False)
    
    def __Str__(self):
        return f'{self.vehicle_name}'

class weather(models.Model):
    weather_condition=models.CharField(choices=env_ch,max_length=128)
    is_active=models.BooleanField(default=False)

    def __Str__(self):
        return f'{self.weather_condition}'

class Rawdata(models.Model):
    vehicleName = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    placeName= models.ForeignKey(Location,on_delete=models.CASCADE)
    total_time=models.PositiveIntegerField()
    break1=models.IntegerField(null=True,blank=True)
    break2=models.IntegerField(null=True,blank=True)
    break3=models.IntegerField(null=True,blank=True)
    break4=models.IntegerField(null=True,blank=True)
    break5=models.IntegerField(null=True,blank=True)
    break6=models.IntegerField(null=True,blank=True)
    break7=models.IntegerField(null=True,blank=True)
    break8=models.IntegerField(null=True,blank=True)
    break9=models.IntegerField(null=True,blank=True)
    break10=models.IntegerField(null=True,blank=True)
    break11=models.IntegerField(null=True,blank=True)
    break12=models.IntegerField(null=True,blank=True)
    result=models.CharField(choices=category_ch,max_length=128)
    time=models.DateTimeField()
    weather_condition=models.CharField(choices=env_ch,max_length=128,null=True,blank=True)

    def __str__(self):
        return f'{self.location} at {self.time}'

class Final(models.Model):
    placeName= models.ForeignKey(Location,on_delete=models.CASCADE)
    chances=models.PositiveIntegerField(blank=True,null=True)
    final_result=models.CharField(choices=category_ch,max_length=128)

    def __str__(self):
        return {self.location} 




