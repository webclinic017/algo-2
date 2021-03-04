from fyers_api import fyersModel
import requests
import json
from flask import jsonify

is_async = False
fyers = fyersModel.FyersModel(is_async)

def getProfile(token): 
    return fyers.get_profile(token)     

def getProfile(token): 
    return fyers.get_profile(token)  

def getFund(token): 
    return fyers.funds(token)  

def placeOrders(token,jsondata):
     return fyers.place_orders(token=token,data = jsondata)      
    
def cancelOrder(token,jsondata):
    return fyers.delete_orders(token=token,data = jsondata)      
    
def exitPositon(token,jsondata):
    return fyers.exit_positions(token=token,data = jsondata)         

def getSbiData():
   url ='https://data.fyers.in/quotes/V2/?symbols=NSE%3ASBIN-EQ&dataReq=1614828467&marketStat=1d60001c3df8a96c0df7954320dcdb52&token_id=gAAAAABgPwCY0zgk7eGVKzA8P_NGr-F1ObKlT4iynOoDSjq4EdN-fLIhMV7moVD0fSbGPPdyrMwMZMZsL8bV8xk0aqJJeU5V5dTl90Vt6JZcQdHhS7lhAD0%3D'
   res = requests.get(url).json()
   data=jsonify(res['d'][0]['v']['lp']) 
   return data.get_data(as_text=True) 
def getBankNiftyData():
   url ='https://data.fyers.in/quotes/V2/?symbols=NSE%3ANIFTY50-INDEX&dataReq=1614828461&marketStat=73798dd18d707d55ff32cfc194400d08&token_id=gAAAAABgPwCY0zgk7eGVKzA8P_NGr-F1ObKlT4iynOoDSjq4EdN-fLIhMV7moVD0fSbGPPdyrMwMZMZsL8bV8xk0aqJJeU5V5dTl90Vt6JZcQdHhS7lhAD0%3D'
   res = requests.get(url).json()
   data=jsonify(res['d'][0]['v']['lp']) 
   return data.get_data(as_text=True)    

 