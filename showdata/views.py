from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,math
import datetime
from django.db.models import Count

from .forms import NameForm
from .models import Location,Vehicle,Rawdata,Final, weather

minimal_time=12;


def index(request):
    return render(request,'index.html')

def raw(request):
    full=Rawdata.objects.all()
    return render(request,'raw.html',{'objects':full})    
    # {'object_list':full}
    

def final(request):
    finalFull=Final.objects.all()
    return render(request,'final.html',{'objects':finalFull})

def wait(request):
    return render(request, 'wait.html')

def test(request):
    if request.method == 'POST':
        form = NameForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            location = data.get('location',None)
            Vehicle_number = data.get('vehicle',None)
            wc=data.get('weather',None)
            Vehicle.objects.create(vehicle_name=Vehicle_number,is_active=True)
            Location.objects.create(place=location,is_active=True)
            weather.objects.create(weather_condition=wc,is_active=True)
            return redirect('showdata:wait')
            
    
    form = NameForm()
    return render(request, 'test.html', {'form': form})


@csrf_exempt
def raw_data_api(request):
    if(request.method == 'POST'):
        data = request.body
        data = json.loads(data)
        
        time_taken=data['endtime']-data['starttime']
        print(time_taken)
        if(time_taken<=minimal_time):
            l=len(data['arraytime'])/12
            breakvalue=[]
            breaks=[]
            for x in range(12):
                breaks.append(math.floor(x*l))
                breakvalue.append(data["arraytime"][breaks[x]])
                # print(f'{breakvalue[x]} at {breaktime[x]}')
                
        forvehicle =Vehicle.objects.filter(is_active=True).first()
        forplace=Location.objects.filter(is_active=True).first()
        forweather=weather.objects.filter(is_active=True).first()
        time=datetime.datetime.now()
        Rawdata.objects.create(weather_condition=forweather,time=time,vehicleName=forvehicle,placeName=forplace,total_time=time_taken,break1=breakvalue[0],break2=breakvalue[1],break3=breakvalue[2],break4=breakvalue[3],break5=breakvalue[4],break6=breakvalue[5],break7=breakvalue[6],break8=breakvalue[7],break9=breakvalue[8],break10=breakvalue[9],break11=breakvalue[10],break12=breakvalue[11])
        placefind=Rawdata.objects.filter(placeName=forplace)
        max=placefind.count()
        
        final=NULL
        for s in set:
            if s.count>max/2:
                percentage=s.count*100/max
                final=s.result
        
        Final.objects.create(placeName=forplace,chances=percentage,result=final)

        
        forvehicle.is_active=False
        forplace.is_active=False
        forweather.is_active=False
        forweather.save()
        forvehicle.save()
        forplace.save()
        

        return redirect('showdata:raw')
    return JsonResponse({'Failed':'Method Not Allowed!'}) 

