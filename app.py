from flask import Flask,Response,render_template,session 
import fyers_login
import Helper
from fyers_api import fyersModel
from orders_model import place_orders
from fyers_model import Fyers_model
from flask import request
import json
import config
from flaskext.mysql import MySQL
import requests
import pandas as pd
import pandas_ta as ta 
from datetime import datetime, timedelta 
from datetime import date
import time

from kiteconnect import KiteTicker, KiteConnect

__token =None
__fyers_model =None

class Config:
    SCHEDULER_API_ENABLED = True
    
app = Flask(__name__)
app.config.from_object(Config())
# initialize scheduler 
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
# scheduler.init_app(app)





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

def storetrade(qty,side,symbol,price,time,indicator):
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()  
   sql = "INSERT INTO trade_book (qty,side,symbol,price,time,indicator) VALUES (%s, %s, %s, %s, %s, %s)"
   val = (qty, side, symbol, price, time,indicator)
   cursor.execute(sql, val)  
   conn.commit()  

@app.route('/indicators',methods=['GET'])      
def indicators():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()  
   start = '2020-04-22'
   end = '2021-04-22'

   symbol = 'MCD'
   # max_holding = 100
   # price=web.DataReader("F", 'yahoo', start, end) 
   # price = price.iloc[::-1]
   # price = price.dropna()
   # close = price['Low'].values
   # up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
   # rsi = talib.RSI(close, timeperiod=14)
   # print("RSI (first 10 elements)\n", rsi[14:24])
   
   return 'sc'
@app.route('/backtesting',methods=['GET'])      
def backtesting():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()   
   url = results[8]
   # url = 'https://data.fyers.in/history/V7/?symbol=NSE%3ANIFTY50-INDEX&resolution=1&from=1618501077&to=1618730097&token_id=gAAAAABge9ueWLukHldUqUSlKaXnx-BjTlI_0k0Pi3_ebRv7au76WeXiKGRb8yvDFyBgFVPAE75-chnNCja34pVF6iicd2Sm_XWMY-N65ZijkOtR1MO2MXs%3D&contFlag=1&marketStat=a295737d89f6b54a967ab7874abe356b&dataReq=1618730038'
   # resjson = requests.get(url).json() 
   # candleinfo = resjson['candles']
   # columns = ['timestamp','Open','High','Low','Close','OI']
   # df = pd.DataFrame(candleinfo, columns=columns)
   # df.reset_index()
   # Open =df['Open']
   # High =df['High']
   # Low =df['Low']
   # Close =df['Close'].values 
   # sma9 = talib.SMA(Close,9)
   # sma21 = talib.SMA(Close,21)
   # rsi = talib.SMA(Close,9)
   # macd, macdsignal, macdhist = talib.MACD(Close, fastperiod=12, slowperiod=26, signalperiod=9) 
   # print(macdhist[-2])
   # macdhist = macdhist[~np.isnan(macdhist)]
   # return render_template('index.html', results=candleinfo)
   
   return 'macd'   

@app.route('/pandasta',methods=['GET'])      
def pandasta():
   cursor.execute("SELECT * from config")
   results = cursor.fetchone()   
   url = results[8]
   # url = 'https://data.fyers.in/history/V7/?symbol=NSE%3ANIFTY50-INDEX&resolution=1&from=1620561415&to=1620790435&token_id=gAAAAABgm0w-XnrWX52NA-h4wMaK6YIxWE25nhMIqpOHjmBVyaiMjh0qIAABt0Z7x_iT0_h8SBgpUTb_qFQX9flwWap_ZvWhrqwpIQ0ma-obBr7UqGOeVqM%3D&contFlag=1&marketStat=75946787eb1b0c34d9effd84d9a48ff3&dataReq=1620790375'
   resjson = requests.get(url).json() 
   candleinfo = resjson['candles']
   columns = ['timestamp','Open','High','Low','Close','OI']
   df = pd.DataFrame(candleinfo, columns=columns)
   df.reset_index()
   Open =df['Open']
   High =df['High']
   Low =df['Low']
   Close =df['Close'].values  
   sma9 = ta.sma(df["Close"], length=9)
   sma21 = ta.sma(df["Close"], length=21)
   print(Close[-1])  
   # print(macdhist[-2])
   # macdhist = macdhist[~np.isnan(macdhist)]
   # return render_template('index.html', results=candleinfo)
   
   return 'macd'  

def task():    
   for i in range(100):
      print('check')
      cursor.execute("SELECT * from config")
      results = cursor.fetchone()   
      url = results[8]
      resjson = requests.get(url).json() 
      if(resjson['s']!='error'): 
         candleinfo = resjson['candles']
         columns = ['timestamp','Open','High','Low','Close','OI']
         df = pd.DataFrame(candleinfo, columns=columns)
         Open =df['Open']
         High =df['High']
         Low =df['Low']
         Close =df['Close'].values 
         sma9 = ta.sma(df["Close"], length=9)
         sma21 = ta.sma(df["Close"], length=21) 
         value = (Open + High + Low + Close)/4
         # print(sma9.iloc[-2])  
         # print(sma21.iloc[-2])  
         if (sma9.iloc[-2] < sma21.iloc[-2]) and (sma9.iloc[-9] > sma21.iloc[-9]):
            print('BUy')
            storetrade(75,1,'nifty',Close.tail(1),1,'sma921') 
         if (sma9.iloc[-2] > sma21.iloc[-2]) and (sma9.iloc[-9] < sma21.iloc[-9]):
            print('Sell') 
            storetrade(75,-1,'nifty',Close[-1],1,'sma921') 
      time.sleep(60)
if __name__ == '__main__': 
   if not app.debug == 'true': 
      task()
      app.run(debug=False,use_reloader=False)
      # app.run(debug=True,use_reloader=True)