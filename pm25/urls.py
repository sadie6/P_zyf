from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^all/', views.all),
    url(r'^pm25_city_hour/', views.pm25_city_hour),
    url(r'^pm25_city_month/', views.pm25_city_month),
 


]