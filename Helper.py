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
   url ='https://data.fyers.in/history/V7/?symbol=NSE%3ANIFTY50-INDEX&resolution=5&from=1617247136&to=1618111196&token_id=gAAAAABgcmnTQYrjcl4lqUoBi5mJ6mfhF_liBN3Qhb06aUeZtecLB3X9oY7gmtWzaQtZ20Ymxp6WgSWUs_p6fU8TysA1nKA69ukE-w3dmfX4nWLRWk-TjS8%3D&contFlag=1&marketStat=b277274b135cabca5e6fa54f64ed0881&dataReq=1618111136'
   res = requests.get(url).json()
   data=jsonify(res['d'][0]['v']['lp']) 
   return data.get_data(as_text=True)    

def getOptinPrice(url): 
   res = requests.get(url).json()
   data=jsonify(res['d'][0]['v']['lp']) 
   return data.get_data(as_text=True)    

 