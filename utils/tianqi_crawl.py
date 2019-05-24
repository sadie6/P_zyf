import requests
import json
import MySQLdb
import re
conn=MySQLdb.connect(host="134.175.34.156",user="root",passwd="123456",db="graduation_zyf", port=3306,charset="utf8")
cursor = conn.cursor()
# data = requests.get("https://www.tianqiapi.com/api/?version=v6&cityid=101110101").text
# data = json.loads(data)
# # print(data,len(data),type(data))
# for k,v in data.items():
# 	print(k,v)
# print(data['data'][0],data['data'][1],len(data['data']))
with open("../static/city.json", 'r') as f:
	citys = json.load(f)

for city in citys[:]:
	cityid = city['id']
	# print(cityid)
	data = requests.get("https://www.tianqiapi.com/api/?version=v6&cityid=%s" %cityid).text
	data = json.loads(data)
	# print(data)
	cityid = data['cityid']
	day = data['date']
	week = data['week']
	updatetime = data['update_time']
	city = data['city']
	wea = data['wea']
	tem = data['tem']
	if not tem:
		tem = 100
	win = data['win']
	win_speed = data['win_speed']
	win_meter = data['win_meter']
	try:
		humidity = re.findall("\d+",data['humidity'])[0]
	except:
		humidity = -1
	try:
		visibility = re.findall("\d+",data['visibility'])[0]
	except:
		visibility = -1
	try:
		pressure = re.findall("\d+",data['pressure'])[0]
	except:
		pressure = -1
	try:
		air = re.findall("\d+",data['air'])[0]
	except:
		air = -1
	try:
		air_pm25 = re.findall("\d+",data['air_pm25'])[0]
	except:
		air_pm25 = -1
	air_level = data['air_level']
	air_tips = data['air_tips']
	alarm = str(data['alarm']).replace('\"', '\'')
	sql = 'insert into pm25_weather(cityid_id, day, week, updatetime, city, wea, tem, win, win_speed, win_meter, humidity, visibility, pressure, air, air_pm25, air_level, air_tips, alarm) \
	values (%s, "%s", "%s", "%s", "%s", "%s",%s, "%s", "%s", "%s", %s, %s,%s, %s, %s,"%s", "%s", "%s")' %(int(cityid), day, week, updatetime, city, wea, int(tem), win, win_speed, win_meter, humidity, visibility, pressure, air, air_pm25, air_level, air_tips, alarm)
	print(sql)
	n = cursor.execute(sql)    

conn.commit()
conn.close()