# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class City(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    cityen = models.CharField(db_column='cityEn', max_length=32)  # Field name made lowercase.
    cityzh = models.CharField(db_column='cityZh', max_length=32)  # Field name made lowercase.
    provinceen = models.CharField(db_column='provinceEn', max_length=32)  # Field name made lowercase.
    provincezh = models.CharField(db_column='provinceZh', max_length=32)  # Field name made lowercase.
    countryen = models.CharField(db_column='countryEn', max_length=32)  # Field name made lowercase.
    countryzh = models.CharField(db_column='countryZh', max_length=32)  # Field name made lowercase.
    leaderen = models.CharField(db_column='leaderEn', max_length=32)  # Field name made lowercase.
    leaderzh = models.CharField(db_column='leaderZh', max_length=32)  # Field name made lowercase.
    lat = models.CharField(max_length=32)
    lon = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'city'


class PlacePm(models.Model):
    id = models.BigAutoField(primary_key=True)
    aqi = models.IntegerField()
    area = models.CharField(max_length=12)
    co = models.FloatField()
    no2 = models.FloatField()
    o3 = models.FloatField()
    pm10 = models.FloatField()
    pm2_5 = models.FloatField()
    position_name = models.CharField(max_length=24)
    so2 = models.FloatField()
    time_point = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'place_PM'


class PlacePm2(models.Model):
    id = models.BigAutoField(primary_key=True)
    aqi = models.IntegerField()
    area = models.CharField(max_length=12)
    co = models.FloatField()
    co_24h = models.FloatField()
    no2 = models.FloatField()
    no2_24h = models.FloatField()
    o3 = models.FloatField()
    o3_24h = models.FloatField()
    o3_8h = models.FloatField()
    o3_8h_24h = models.FloatField()
    pm10 = models.FloatField()
    pm10_24h = models.FloatField()
    pm2_5 = models.FloatField()
    pm2_5_24h = models.FloatField()
    position_name = models.CharField(max_length=24)
    primary_pollutant = models.CharField(max_length=256)
    quality = models.CharField(max_length=5)
    so2 = models.FloatField()
    so2_24h = models.FloatField()
    station_code = models.CharField(max_length=12)
    time_point = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'place_PM2'


class PlacePmCoordinates(models.Model):
    city = models.CharField(max_length=50)
    coordinates = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'place_PM_coordinates'



class Weather(models.Model):
	id = models.BigAutoField(primary_key=True)
	cityid = models.ForeignKey(City, on_delete=models.CASCADE)
	city = models.CharField(max_length=10)
	updatetime = models.TimeField()
	day = models.DateTimeField()
	week = models.CharField(max_length=8)
	wea = models.CharField(max_length=6)
	tem = models.IntegerField()
	win = models.CharField(max_length=6)
	win_speed = models.CharField(max_length=8)
	win_meter = models.CharField(max_length=12)
	humidity = models.IntegerField()
	visibility = models.IntegerField()
	pressure = models.IntegerField()
	air = models.IntegerField()
	air_pm25 = models.IntegerField()
	air_level = models.CharField(max_length=6)
	air_tips = models.TextField()
	alarm = models.TextField()





