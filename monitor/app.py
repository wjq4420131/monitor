#-*-coding:utf8 -*-...
import web
import json
from datetime import datetime

urls = (
	'/','Monitor',
	'/Monitor/(\d+)','Monitor',
	'/list_group','List_group',
	'/details/(\d+)','Details'
)


render = web.template.render('templates/')
db = web.database(dbn="mysql",user="root",passwd="123456",charset="utf8",db="core")


#分组展示页面
class List_group():
	def GET(self):
		listgroup = db.select("fenzu")
		return render.list_group(listgroup)


#监控数据展示页面
class Monitor():
	def GET(self):
		monitor_data = db.query(""" select f.group_id as id, f.group_name as organ_name ,count(DISTINCT(d.ipaddr)) as device_count,

									COUNT(CASE WHEN w.alarm_type = 1 AND w.create_time>=DATE_SUB(NOW(),INTERVAL 10 MINUTE) THEN w.id END ) AS yiban,

									COUNT(CASE WHEN w.alarm_type = 2 AND w.create_time>=DATE_SUB(NOW(),INTERVAL 10 MINUTE)  THEN w.id END ) AS yanzhong 

									FROM fenzu f left join  waring  w  on f.group_id=w.group_id  left join device d on d.group_Id=f.group_id  GROUP BY f.group_id;

								""")

		return render.monitor(monitor_data)



#时间序列化类
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



#详情页
class Details():
	def GET(self,group_id):
		group_id = int(group_id)
		print group_id
		group_data = db.select('waring',where='group_id=$group_id and create_time>=DATE_SUB(NOW(),INTERVAL 10 MINUTE)' ,vars=locals())

		# list=[]
		# for d in group_data:
		# 	list.append(d)

		# web.header('Content-Type', 'application/json')

		# a = json.dumps(list,cls=ComplexEncoder,ensure_ascii=True)
		# return a



		list = []
		for data in group_data:
			if data.alarm_type==2:
				data.alarm_name="严重告警"
			else:
				data.alarm_name="一般告警"

			list.append(data)
		

		return render.details(list)


if __name__ =="__main__":
	app = web.application(urls,globals())
	app.run()