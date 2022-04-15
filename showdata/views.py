from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,math
import datetime
from django.db.models import Count

from .forms import NameForm
from .models import Location,Vehicle,Rawdata,Final, weather,Entity,Tempdata

minimal_time=5
avg_time=20
min_count=5
avg_count=20



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


def raw_data_api(request):
    if(request.method == 'POST'):
        data = request.body
        data = json.loads(data)
        
        obj=Entity.objects.filter(is_active=True)
        starttime=obj.starttime
        time_taken=datetime.datetime.now()-starttime
        counts=data['fluctuation']

        forvehicle =Vehicle.objects.filter(is_active=True).first()
        forplace=Location.objects.filter(is_active=True).first()
        forweather=weather.objects.filter(is_active=True).first()
        forentity=Entity.objects.filter(is_active=True).first()

        if(counts<min_count):
            if(time_taken<= minimal_time):
                result="small_speedbreaker"
            
            elif(time_taken>=minimal_time and time_taken<=avg_time):
                result="speedbreaker"

            else:
                result="ascend_descend"
        
        elif(counts>=min_count and counts<=avg_count):
            if(time_taken<= minimal_time):
                result="high_speedbreaker";
            
            elif(time_taken>=minimal_time and time_taken<=avg_time):
                result="speedbreaker"

            else:
                result="big_speedbreaker"

        elif(counts>avg_count):
            if(time_taken<= minimal_time):
                result="bump or_pit";
            
            elif(time_taken>=minimal_time and time_taken<=avg_time):
                result="rough_surface"

            else:
                result="extreme_condition"


        Rawdata.objects.create(weather_condition=forweather,vehicleName=forvehicle,placeName=forplace,total_time=time_taken,fluctuation=counts,result=result)
        placefind=Rawdata.objects.filter(placeName=forplace)
        max=placefind.count()
        
        # final=NULL
        # for s in set:
        #     if s.count>max/2:
        #         percentage=s.count*100/max
        #         final=s.result
        mapp = {}
        for i in placefind:
            mapp[i.result] = mapp.get(i.result,0) + 1
        
        maxValue = 0
        maxCount = 0
        for x,y in mapp.items():
            if(maxCount>y):
                maxValue = x
                maxCount = y

        percentage=maxCount/max*100
        final=maxValue

        Final.objects.update_or_create(placeName=forplace,chances=percentage,result=final)

        
        forvehicle.is_active=False
        forplace.is_active=False
        forweather.is_active=False
        forentity.is_active=False
        forweather.save()
        forvehicle.save()
        forplace.save()
        forentity.save()
        

        return redirect('showdata:raw')
    return JsonResponse({'Failed':'Method Not Allowed!'}) 


@csrf_exempt
def receive_dist_data(request):
    if(request.method == "POST"):
        data = request.body
        data = json.loads(data)
        print(data)
        # get Vehicle and location
        vehicle = Vehicle.objects.filter(is_active=True).first()
        location = Location.objects.filter(is_active=True).first()
        print(vehicle,location)
        obj,created = Entity.objects.get_or_create(vehicleName=vehicle,placeName=location,is_active=True)

        curr_count = obj.data.all().count()
        curr_count+=1
        data_obj = Tempdata.objects.create(distance=data['distance'],count=curr_count)
        obj.data.add(data_obj)
    
        return JsonResponse({"Success":"Data Added!"})
    return JsonResponse({'Failed':'Method Not Allowed!'}) 
