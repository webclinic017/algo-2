from fyers_api import fyersModel

class Fyers_model :

    def __init__(self,token):
        self.token = token
        is_async = False
        self.fyersmodel =fyersModel.FyersModel(is_async)

    def getFyersModel(self):
        return self.fyersmodel 

    def getToken(self):
        return self.token    
    
    def getProfile(self):
        return self.fyersmodel.get_profile(token=self.token)    

    def place_orders(self,jsondata):
        return self.fyersmodel.place_orders(token=self.token,data = jsondata)      
    
    def cancelOrder(self,jsondata):
        return self.fyersmodel.delete_orders(token=self.token,data = jsondata)      
    
    def exitPositon(self,jsondata):
        return self.fyersmodel.exit_positions(token=self.token,data = jsondata)      