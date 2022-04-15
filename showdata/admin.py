from django.contrib import admin
from showdata.models import Vehicle,Location,Rawdata,Final,weather

admin.site.register(Vehicle)
admin.site.register(Location)
admin.site.register(Rawdata)
admin.site.register(Final)
admin.site.register(weather)