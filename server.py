#other imports we need
import time, os, json, re
import datetime, pytz, sys, 
import threading, pymysql, multiprocessing

#flask imports
from flask import Flask,render_template
from flask import request,Response,redirect,url_for,jsonify
from flask_caching import Cache

#model classes
from sensor_model import Sensor

app = Flask(__name__)
global DATABASE_USER
global DATABASE_PASSWORD
global DATABASE_DB
global DATABASE_HOST

semaphore = multiprocessing.Semaphore(50)

# dev db info

'''
DATABASE_USER = 'admin'
DATABASE_PASSWORD = 'password'
DATABASE_DB = 'temps'
DATABASE_HOST = 'localhost'
'''

with open('/home/ubuntu/db_info.json', 'r') as db_info:
    data=db_info.read()
obj = json.loads(data)

DATABASE_USER = str(obj['DATABASE_USER'])
DATABASE_PASSWORD = str(obj['DATABASE_PASSWORD'])
DATABASE_DB = str(obj['DATABASE_DB'])
DATABASE_HOST = str(obj['DATABASE_HOST'])

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
        select1 = "select temp,humd,UNIX_TIMESTAMP(date) * 1000 as 'unixTime' ,convert_tz(date,'+00:00','-05:00') as 'normalTime' from tempdata2 order by id desc limit 1"
        tempData1 = query_db(select1)
    except Exception as e:
        return jsonify(e), 500
    s = Sensor(tempData1[0]['temp'],tempData1[0]['humd'],tempData1[0]['unixTime'],tempData1[0]['normalTime'])

    return {"temp":s.temp,"humid":s.humid,"last_updated":s.time_unix,"last_updated_normal": s.time_normal}, 200

@app.route("/getTemp2", methods=['GET'])
def getTemp2():
    try:
        select2 = "select temp,humd,UNIX_TIMESTAMP(date) * 1000 as 'unixTime' ,convert_tz(date,'+00:00','-05:00') as 'normalTime' from tempdata3 order by id desc limit 1"
        tempData2 = query_db(select2)
    except Exception as e:
        return jsonify(e), 500
    s = Sensor(tempData2[0]['temp'],tempData2[0]['humd'],tempData2[0]['unixTime'],tempData2[0]['normalTime'])

    return {"temp":s.temp,"humid":s.humid,"last_updated":s.time_unix,"last_updated_normal":s.time_normal}, 200

@app.route('/temp1Chart')
@cache.cached(timeout=600) #600 seconds = 10 mins
def chart1():
    select_temp_data = "select temp,humd, convert_tz(date,'+00:00','-05:00') as 'normalTime'  from(select * from tempdata2 order by id desc limit 60)Var1 order by id asc"
    data2 = query_db(select_temp_data)
    x_val = [normalTime['normalTime'] for normalTime in data2]
    y_val = [temp['temp'] for temp in data2] #temp
    y_val2 = [humd['humd'] for humd in data2] #humid
    page_title = "Basement Sensor Chart"
    
    return render_template("chart.html",**locals())

@app.route('/temp2Chart')
@cache.cached(timeout=600) #600 seconds = 10 mins
def chart2():
    select_temp_data = "select temp,humd, convert_tz(date,'+00:00','-05:00') as 'normalTime' from(select * from tempdata3 order by id desc limit 60)Var1 order by id asc"
    data2 = query_db(select_temp_data)
    x_val = [normalTime['normalTime'] for normalTime in data2]
    y_val = [temp['temp'] for temp in data2] #temp
    y_val2 = [humd['humd'] for humd in data2] #humid
    page_title = "Bedroom Sensor Chart"

    return render_template("chart.html",**locals())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def query_db(query):

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST, 
    user=DATABASE_USER, password=DATABASE_PASSWORD, 
    database=DATABASE_DB,   
    cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            with semaphore:
                cursor.execute(query)
                query_result = cursor.fetchall()
        
    return query_result
