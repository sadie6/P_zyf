from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models.aggregates import Count,Sum,Avg
from pm25.models import City, PlacePm, PlacePm2, PlacePmCoordinates, Weather
from django.views.decorators.cache import cache_page
import numpy as np
import random
import time
import math
import json
# import re

# Create your views here.

# citys = ['长沙', '北京', '上海', '杭州', '广州', '成都', '福州', '南宁', '沈阳', '哈尔滨']

# citys = re.findall(r"name: '(.*?)',", citys)
# print(citys)

citys = ['海门', '鄂尔多斯', '招远', '舟山', '齐齐哈尔', '盐城', '赤峰', '青岛', '乳山',
 '金昌', '泉州', '莱西', '日照', '胶南', '南通', '拉萨', '云浮', '梅州', '文登',
 '上海', '攀枝花', '威海', '承德', '厦门', '汕尾', '潮州', '丹东', '太仓', '曲靖\
', '烟台', '福州', '瓦房店', '即墨', '抚顺', '玉溪', '张家口', '阳泉', '莱州', '\
湖州', '汕头', '昆山', '宁波', '湛江', '揭阳', '荣成', '连云港', '葫芦岛', '常熟\
', '东莞', '河源', '淮安', '泰州', '南宁', '营口', '惠州', '江阴', '蓬莱', '韶关\
', '嘉峪关', '广州', '延安', '太原', '清远', '中山', '昆明', '寿光', '盘锦', '长\
治', '深圳', '珠海', '宿迁', '咸阳', '铜川', '平度', '佛山', '海口', '江门', '章\
丘', '肇庆', '大连', '临汾', '吴江', '石嘴山', '沈阳', '苏州', '茂名', '嘉兴', '\
长春', '胶州', '银川', '张家港', '三门峡', '锦州', '南昌', '柳州', '三亚', '自贡\
', '吉林', '阳江', '泸州', '西宁', '宜宾', '呼和浩特', '成都', '大同', '镇江', '\
桂林', '张家界', '宜兴', '北海', '西安', '金坛', '东营', '牡丹江', '遵义', '绍兴\
', '扬州', '常州', '潍坊', '重庆', '台州', '南京', '滨州', '贵阳', '无锡', '本溪\
', '克拉玛依', '渭南', '马鞍山', '宝鸡', '焦作', '句容', '北京', '徐州', '衡水',
 '包头', '绵阳', '乌鲁木齐', '枣庄', '杭州', '淄博', '鞍山', '溧阳', '库尔勒', '\
安阳', '开封', '济南', '德阳', '温州', '九江', '邯郸', '临安', '兰州', '沧州', '\
临沂', '南充', '天津', '富阳', '泰安', '诸暨', '郑州', '哈尔滨', '聊城', '芜湖',
 '唐山', '平顶山', '邢台', '德州', '济宁', '荆州', '宜昌', '义乌', '丽水', '洛阳\
', '秦皇岛', '株洲', '石家庄', '莱芜', '常德', '保定', '湘潭', '金华', '岳阳', '\
长沙', '衢州', '廊坊', '菏泽', '合肥','武汉', '大庆']


T = time.localtime(time.time())
M = 60 - T.tm_min

@cache_page(M*60)
def index(request):
	localtime = time.localtime(time.time())
	t1 = time.strftime("%Y-%m-%d %H:00:00", localtime) 
	year = localtime.tm_year
	month = localtime.tm_mon
	day = localtime.tm_mday
	hour = int(localtime.tm_hour) - 1
	if hour == -1:
		day -= 1
		hour = 23

	if month < 10:
		_month = '0' + str(month)
	else:
		_month = month
	if day < 10:
		_day = '0' + str(day)
	else:
		_day = day
	if hour < 10:
		_hour = '0' + str(hour)
	else:
		_hour = hour

	data = {}
	# data['map'] = {}
	for city in citys:
		pm_data = PlacePm.objects.filter(area = city, time_point = '%s-%s-%s %s:00:00' %(year, _month, _day, _hour))
		data[city] = pm_data.aggregate(Avg("aqi"))['aqi__avg']

	# data_hour = [[],[],[],[],[],[],[]]
	# hours = []
	# for i in range(11):
	# 	if(hour - 1) < -1:
	# 		hour = 23
	# 		day -= 1
	# 	if month < 10:
	# 		_month = '0' + str(month)
	# 	else:
	# 		_month = month
	# 	if day < 10:
	# 		_day = '0' + str(day)
	# 	else:
	# 		_day = day
	# 	if hour < 10:
	# 		_hour = '0' + str(hour)
	# 	else:
	# 		_hour = hour

	# 	pm_data = PlacePm.objects.filter(area = '长沙', time_point = '%s-%s-%s %s:00:00' %(year, _month, _day, _hour))
	# 	data_hour[0].append(pm_data.aggregate(Avg("aqi"))['aqi__avg']) 
	# 	data_hour[1].append(pm_data.aggregate(Avg("co"))['co__avg']) 
	# 	data_hour[2].append(pm_data.aggregate(Avg("no2"))['no2__avg']) 
	# 	data_hour[3].append(pm_data.aggregate(Avg("o3"))['o3__avg']) 
	# 	data_hour[4].append(pm_data.aggregate(Avg("pm10"))['pm10__avg']) 
	# 	data_hour[5].append(pm_data.aggregate(Avg("pm2_5"))['pm2_5__avg']) 
	# 	data_hour[6].append(pm_data.aggregate(Avg("so2"))['so2__avg']) 
	# 	hours.append([day, hour])
		
	# 	hour -= 1


	# data_month = [[],[],[],[],[],[],[]]
	# months = []
	# for i in range(12):
	# 	if (month - 1) < 0:
	# 		month = 12
	# 		year -= 1
	# 	pm_data = PlacePm.objects.filter(area = '长沙', time_point__year=year, time_point__month = month)
	# 	data_month[0].append(pm_data.aggregate(Avg("aqi"))['aqi__avg']) 
	# 	data_month[1].append(pm_data.aggregate(Avg("co"))['co__avg']) 
	# 	data_month[2].append(pm_data.aggregate(Avg("no2"))['no2__avg']) 
	# 	data_month[3].append(pm_data.aggregate(Avg("o3"))['o3__avg']) 
	# 	data_month[4].append(pm_data.aggregate(Avg("pm10"))['pm10__avg']) 
	# 	data_month[5].append(pm_data.aggregate(Avg("pm2_5"))['pm2_5__avg']) 
	# 	data_month[6].append(pm_data.aggregate(Avg("so2"))['so2__avg']) 
	# 	months.append([year, month])
		
	# 	month -= 1

	# data['data_hour'] = data_hour
	# data['hours'] = hours
	# data['data_month'] = data_month
	# data['months'] = months
		


	return HttpResponse(json.dumps(data))


@cache_page(M*60)
def pm25_city_hour(request):
	localtime = time.localtime(time.time())
	t1 = time.strftime("%Y-%m-%d %H:00:00", localtime) 
	year = localtime.tm_year
	month = localtime.tm_mon
	day = localtime.tm_mday
	hour = int(localtime.tm_hour) - 1
	if hour == -1:
		day -= 1
		hour = 23

	city = request.GET.get("city", None)
	data = {}
	if city:
		data_hour = [[],[],[],[],[],[],[]]
		hours = []
		for i in range(11):
			if(hour - 1) < -1:
				hour = 23
				day -= 1
			if month < 10:
				_month = '0' + str(month)
			else:
				_month = month
			if day < 10:
				_day = '0' + str(day)
			else:
				_day = day
			if hour < 10:
				_hour = '0' + str(hour)
			else:
				_hour = hour

			pm_data = PlacePm.objects.filter(area = city, time_point = '%s-%s-%s %s:00:00' %(year, _month, _day, _hour))
			data_hour[0].append(pm_data.aggregate(Avg("aqi"))['aqi__avg']) 
			data_hour[1].append(pm_data.aggregate(Avg("co"))['co__avg']) 
			data_hour[2].append(pm_data.aggregate(Avg("no2"))['no2__avg']) 
			data_hour[3].append(pm_data.aggregate(Avg("o3"))['o3__avg']) 
			data_hour[4].append(pm_data.aggregate(Avg("pm10"))['pm10__avg']) 
			data_hour[5].append(pm_data.aggregate(Avg("pm2_5"))['pm2_5__avg']) 
			data_hour[6].append(pm_data.aggregate(Avg("so2"))['so2__avg']) 
			hours.append(str(day) + '日' + str(_hour) + '时')
			
			hour -= 1



		# data_month = [[],[],[],[],[],[],[]]
		# months = []
		# for i in range(12):
		# 	if (month - 1) < 0:
		# 		month = 12
		# 		year -= 1
		# 	pm_data = PlacePm.objects.filter(area = city, time_point__year=year, time_point__month = month)
		# 	data_month[0].append(pm_data.aggregate(Avg("aqi"))['aqi__avg']) 
		# 	data_month[1].append(pm_data.aggregate(Avg("co"))['co__avg']) 
		# 	data_month[2].append(pm_data.aggregate(Avg("no2"))['no2__avg']) 
		# 	data_month[3].append(pm_data.aggregate(Avg("o3"))['o3__avg']) 
		# 	data_month[4].append(pm_data.aggregate(Avg("pm10"))['pm10__avg']) 
		# 	data_month[5].append(pm_data.aggregate(Avg("pm2_5"))['pm2_5__avg']) 
		# 	data_month[6].append(pm_data.aggregate(Avg("so2"))['so2__avg']) 
		# 	months.append(str(year) + '年' + str(month) + '月')
			
		# 	month -= 1

		data['data_hour'] = data_hour
		data['hours'] = hours
		# data['data_month'] = data_month
		# data['months'] = months


	return HttpResponse(json.dumps(data))


@cache_page(3600*10)
def pm25_city_month(request):
	localtime = time.localtime(time.time())
	t1 = time.strftime("%Y-%m-%d %H:00:00", localtime) 
	year = localtime.tm_year
	month = localtime.tm_mon
	
	city = request.GET.get("city", None)
	data = {}
	if city:
		data_month = [[],[],[],[],[],[],[]]
		months = []
		for i in range(12):
			if (month - 1) < 0:
				month = 12
				year -= 1
			pm_data = PlacePm.objects.filter(area = city, time_point__year=year, time_point__month = month)
			data_month[0].append(pm_data.aggregate(Avg("aqi"))['aqi__avg']) 
			data_month[1].append(pm_data.aggregate(Avg("co"))['co__avg']) 
			data_month[2].append(pm_data.aggregate(Avg("no2"))['no2__avg']) 
			data_month[3].append(pm_data.aggregate(Avg("o3"))['o3__avg']) 
			data_month[4].append(pm_data.aggregate(Avg("pm10"))['pm10__avg']) 
			data_month[5].append(pm_data.aggregate(Avg("pm2_5"))['pm2_5__avg']) 
			data_month[6].append(pm_data.aggregate(Avg("so2"))['so2__avg']) 
			months.append(str(year) + '年' + str(month) + '月')
			
			month -= 1

		
		data['data_month'] = data_month
		data['months'] = months


	return HttpResponse(json.dumps(data))






@cache_page(3600*10)
def all(request):
	localtime = time.localtime(time.time())
	t1 = time.strftime("%Y-%m-%d %H:00:00", localtime) 
	year = localtime.tm_year
	month = localtime.tm_mon

	data_month = [[],[],[],[],[],[],[]]
	months = []

	data = {}
	for i in range(12):
			if (month - 1) < 0:
				month = 12
				year -= 1
			pm_data = PlacePm.objects.filter(time_point__year=year, time_point__month = month)
			data_month[0].append(pm_data.aggregate(Avg("aqi"))['aqi__avg']) 
			data_month[1].append(pm_data.aggregate(Avg("co"))['co__avg']) 
			data_month[2].append(pm_data.aggregate(Avg("no2"))['no2__avg']) 
			data_month[3].append(pm_data.aggregate(Avg("o3"))['o3__avg']) 
			data_month[4].append(pm_data.aggregate(Avg("pm10"))['pm10__avg']) 
			data_month[5].append(pm_data.aggregate(Avg("pm2_5"))['pm2_5__avg']) 
			data_month[6].append(pm_data.aggregate(Avg("so2"))['so2__avg']) 
			months.append(str(year) + '年' + str(month) + '月')
			
			month -= 1

	
	data['data_month'] = data_month
	data['months'] = months

	return HttpResponse(json.dumps(data))













