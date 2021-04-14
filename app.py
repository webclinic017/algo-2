from flask import Flask,Response,render_template,session
import fyers_login
import Helper
from fyers_api import fyersModel
from orders_model import place_orders
from fyers_model import Fyers_model
from flask import request
import sys
import json
import jsonify
import config
from flaskext.mysql import MySQL
import requests
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta 
from datetime import date 
import time

from kiteconnect import KiteTicker, KiteConnect

__token =None
__fyers_model =None
app = Flask(__name__)
app.secret_key = 'asdsssssssaaaa'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'eageskoo_nse'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ashok@2342'
app.config['MYSQL_DATABASE_DB'] = 'eageskoo_nse'
app.config['MYSQL_DATABASE_HOST'] = '162.214.94.136'
mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()

@app.route('/')
def home(): 
   return 'welcome'

@app.route('/data')
def data(): 
   cursor.execute("SELECT * from nifty")
   results = cursor.fetchone()  
   return render_template('index.html', results=results)

@app.route('/login')
def login():
   return fyers_login.getLoginHtml()

@app.route('/logout')
def logout():
   session.pop('token', None)
   sql = " UPDATE config SET token = %s WHERE id = %s"
   val = ('', 1) 
   cursor.execute(sql, val)  
   conn.commit()
   return 'logout'

@app.route('/sbi')
def getSbiData():  
   data =Helper.getSbiData()  
   return data

@app.route('/loginstatus')
def loginstatus():
    token = request.args.get('access_token') 
    token = session['token'] = token 
    sql = " UPDATE config SET token = %s WHERE id = %s"
    val = (token, 1) 
    cursor.execute(sql, val)  
    conn.commit()  
    return 'success'

@app.route('/profile',methods=['GET','POST'])
def getProfile(): 
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()   
   token = results[4]
   return Helper.getProfile(token)

@app.route('/fund',methods=['GET','POST'])
def getFund():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()   
   token = results[4]
   return Helper.getFund(session['token']) 

@app.route('/token',methods=['GET','POST'])
def getToken():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()   
   token = results[4]
   return token 

@app.route('/session_token',methods=['GET','POST'])
def getSessionToken():
   token = session['token'] 
   return token        

@app.route('/exit',methods=['GET','POST'])
def exitPositon():
   token = session['token'] 
   json_data =request.json
   id =json_data["id"]
   orderinfo = place_orders()
   orderinfo.setSymbole(id) 
   return Helper.exitPositon(session['token'],orderinfo.getJsonStructure()) 

@app.route('/webhook',methods=['post'])
def webhook():
   data =json.loads(request.data)
   if data['password'] != config.WEBHOOK_PASSWORD:
      return {
      "code":"error",
      "message":"Password Not Match"
      }
   price =Helper.getSbiData()
   json_data =request.json
   symbol = "NSE:" + str(json_data["symbol"]) + "-EQ"
   types =json_data["type"]
   time =json_data["time"]   
   qty =json_data["qty"]
   sql = "INSERT INTO trade_book (qty,type,symbol,price,time) VALUES (%s, %s, %s, %s, %s)"
   val = (qty, types, symbol, price, time)
   cursor.execute(sql, val)  
   conn.commit()  
   return {
      "code":200,
      "data":data,
      "message":"Success"
      }
@app.route('/webhookb',methods=['post'])      
def webhookB():
   data =json.loads(request.data)
   if data['password'] != config.WEBHOOK_PASSWORD:
      return {
      "code":"error",
      "message":"Password Not Match"
      }
   price =Helper.getBankNiftyData()
   json_data =request.json
   symbol = "NSE:" + str(json_data["symbol"]) + "-EQ"
   types =json_data["type"]
   time =json_data["time"]   
   qty =json_data["qty"]
   sql = "INSERT INTO trade_book (qty,type,symbol,price,time) VALUES (%s, %s, %s, %s, %s)"
   val = (qty, types, symbol, price, time)
   cursor.execute(sql, val)  
   conn.commit()  
   return {
      "code":200,
      "data":data,
      "message":"Success"
      }      

@app.route('/place-order',methods=['GET','POST'])
def placeOrder():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()   
   token = results[4]  
   json_data =request.json
   if json_data['password'] != config.WEBHOOK_PASSWORD:
      return {
      "code":"error",
      "message":"Password Not Match"
      }
   # symbol = "NSE:" + str(json_data["symbol"]) + "-EQ"
   # price =json_data["price"]
   # qty =json_data["qty"]
   # type =json_data["type"]
   # side =json_data["side"]
   # orderinfo = place_orders()
   # orderinfo.setSymbole(symbol)
   # orderinfo.setSymbole(symbol)
   # orderinfo.setSymbole(symbol)
   return Helper.placeOrders(token,json_data)

@app.route('/place-order-op',methods=['GET','POST'])
def placeOrderOp(): 
   json_data =request.json
   if json_data['password'] != config.WEBHOOK_PASSWORD:
      return {
      "code":"error",
      "message":"Password Not Match"
      }
   json_data['password'] ='ad'   
   return Helper.getStrick() 
   return Helper.placeOrders(token,json_data)  


@app.route('/paper-trade',methods=['post'])      
def papertrade():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()  
   data =json.loads(request.data) 
   url = results[data['trade_type']]
   if data['password'] != config.WEBHOOK_PASSWORD:
      return {
      "code":"error",
      "message":"Password Not Match"
      }
   price =Helper.getOptinPrice(url)
   json_data =request.json
   symbol = str(json_data["symbol"])
   side =json_data["side"]
   time =json_data["time"]   
   qty =json_data["qty"]
   sql = "INSERT INTO trade_book (qty,side,symbol,price,time) VALUES (%s, %s, %s, %s, %s)"
   val = (qty, side, symbol, price, time)
   cursor.execute(sql, val)  
   conn.commit()  
   return {
      "code":200,
      "data":data,
      "message":"Success"
      }   

@app.route('/indicators',methods=['GET'])      
def indicators():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()  
   start = '2020-04-22'
   end = '2021-04-22'

   symbol = 'MCD'
   max_holding = 100
   price=web.DataReader("F", 'yahoo', start, end) 
   price = price.iloc[::-1]
   price = price.dropna()
   close = price['Low'].values
   up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
   rsi = talib.RSI(close, timeperiod=14)
   print("RSI (first 10 elements)\n", rsi[14:24])
   
   return 'sc'    
@app.route('/get-data',methods=['GET'])      
def getdata():
   userid=''
   timeframe='minute'
   auth_token='enctoken d6vMDOm5PwfpI9HOq8MNsOjvWxFExZs7/BiodiHlQbU8+/mskJhqaWLadToc3m1I4R/9JYH/OfxuJLMy04MwZ0ss6GHZcw=='
   ciqrandom='1617468866644'
   headers={'Authorization':auth_token}
   from_date =''
   from_date =date(2020,4,10)
   to_date =date(2020,4,9)
   url = 'https://data.fyers.in/history/V7/?symbol=NSE%3ANIFTY50-INDEX&resolution=5&from=1617247136&to=1618111196&token_id=gAAAAABgcmnTQYrjcl4lqUoBi5mJ6mfhF_liBN3Qhb06aUeZtecLB3X9oY7gmtWzaQtZ20Ymxp6WgSWUs_p6fU8TysA1nKA69ukE-w3dmfX4nWLRWk-TjS8%3D&contFlag=1&marketStat=b277274b135cabca5e6fa54f64ed0881&dataReq=1618111136'
   resjson = requests.get(url,headers=headers).json() 
   candleinfo = resjson['candles']
   columns = ['timestamp','Open','High','Low','Close','OI']
   df = pd.DataFrame(candleinfo, columns=columns)
   Open =df['Open']
   High =df['High']
   Low =df['Low']
   Close =df['Close'].values
   timestamp =df['timestamp'] 
   date_time=[]
   for times in timestamp:
      date_time = datetime.fromtimestamp(times) 

   sma9 = talib.SMA(Close,9)
   sma21 = talib.SMA(Close,21)
   rsi = talib.SMA(Close,9)
   macd = talib.MACD(Close, fastperiod=12, slowperiod=26, signalperiod=9)
   value = (Open + High + Low + Close)/4
    
   while True:    
   if (datetime.now().secound==0) and (datetime.now().minute % 5 == 0):
      if (sma9[-9] < sma21[-9]) and (sma9[-8] > sma21[-8]):
         print('BUy') 
         
   if (datetime.now().secound==0) and (datetime.now().minute % 5 == 0):
      if (sma9[-9] < sma21[-9]) and (sma9[-8] > sma21[-8]):
         print('Sell')
            
     
   print("RSI (first 10 elements)\n", date_time) 
   print(date_time)
   return render_template('tradingview.html', resjson=candleinfo)
if __name__ == '__main__':
   app.run(debug=True)