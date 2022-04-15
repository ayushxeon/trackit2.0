from django.urls import path
from . import views

app_name = 'showdata'

urlpatterns=[
    path('',views.index,name='index'),
    path('rawdb/',views.raw,name='raw'),
    path('finaldb/',views.final,name='final'),
    path('testing/',views.test,name='test'),
    path('api/collect/',views.raw_data_api,name='collect'),
    path('waiting/',views.wait,name='wait'),
]