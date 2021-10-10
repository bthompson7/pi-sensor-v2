#other imports we need
import time, os, json, re
import datetime, pytz, sys, threading

#flask imports
from flask import Flask,render_template
from flask import request,Response,redirect,url_for,jsonify
from flask_caching import Cache

#mysql
from flaskext.mysql import MySQL

#model classes
from sensor_model import Sensor

app = Flask(__name__)
sema = threading.Semaphore()

global mysql
mysql = MySQL()


with open('db_info.json', 'r') as db_info:
    data=db_info.read()
obj = json.loads(data)

app.config['MYSQL_DATABASE_USER'] = str(obj['DATABASE_USER'])
app.config['MYSQL_DATABASE_PASSWORD'] = str(obj['DATABASE_PASSWORD'])
app.config['MYSQL_DATABASE_DB'] = str(obj['DATABASE_DB'])
app.config['MYSQL_DATABASE_HOST'] = str(obj['DATABASE_HOST'])
mysql.init_app(app)

#cache config.
config = {
    "DEBUG": False,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app.config.from_mapping(config)
cache = Cache(app)

@app.route('/')
def main():
   return render_template("index.html")

@app.route("/getTemp1", methods=['GET'])
def getTemp1():
	try:
		select1 = "select temp,humd,UNIX_TIMESTAMP(date),convert_tz(date,'+00:00','-05:00') from tempdata2 order by id desc limit 1"
		tempData1 = query_db(select1)

	except Exception as e:
		return jsonify(e), 500

	s = Sensor(tempData1[0][0],tempData1[0][1],tempData1[0][2],tempData1[0][3])
	return {"temp":s.temp,"humid":s.humid,"last_updated":s.time_unix,"last_updated_normal":s.time_normal}, 200

@app.route("/getTemp2", methods=['GET'])
def getTemp2():
	try:
		select2 = "select temp,humd,UNIX_TIMESTAMP(date),convert_tz(date,'+00:00','-05:00') from tempdata3 order by id desc limit 1"
		tempData2 = query_db(select2)
	except Exception as e:
		return jsonify(e), 500

	s = Sensor(tempData2[0][0],tempData2[0][1],tempData2[0][2],tempData2[0][3])
	return {"temp":s.temp,"humid":s.humid,"last_updated":s.time_unix,"last_updated_normal":s.time_normal}, 200

@app.route('/temp1Chart')
@cache.cached(timeout=600) #600 seconds = 10 mins
def chart1():
   select_temp_data = "select * from(select * from tempdata2 order by id desc limit 60)Var1 order by id asc"
   data2 = query_db(select_temp_data)

   x_val = [date[3] for date in data2]
   y_val = [temp[1] for temp in data2] #temp
   y_val2 = [humd[2] for humd in data2] #humid
   page_title = "Basement Sensor Chart"

   return render_template("chart.html",**locals())

@app.route('/temp2Chart')
@cache.cached(timeout=600) #600 seconds = 10 mins
def chart2():

   select_temp_data = "select * from(select * from tempdata3 order by id desc limit 60)Var1 order by id asc"
   data2 = query_db(select_temp_data)

   x_val = [date[3] for date in data2]
   y_val = [temp[1] for temp in data2] #temp
   y_val2 = [humd[2] for humd in data2] #humid
   page_title = "Bedroom Sensor Chart"
   return render_template("chart.html",**locals())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def query_db(query):
    sema.acquire()

    try:
        query_result = "ok"
        db = mysql.get_db()
        cursor = db.cursor()
        parsed_query = re.split("\s",query)

        if parsed_query[0].lower() == "select":
            cursor.execute(query)
            db.commit()
            query_result = cursor.fetchall()
        else:
            cursor.execute(query)
            db.commit()

    except Exception as e:
        print("error querying the databse", e)
        raise Exception(e)
    finally:
        sema.release()

    return query_result