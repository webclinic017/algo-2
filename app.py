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

if __name__ == '__main__':
   app.run()