import json

class place_orders :

    def __init__(self):
        self.symbol = None
        self.qty = 0
        self.type = 1
        self.side = 1
        self.productType = 'INTRADAY'
        self.limitPrice = 0
        self.stopPrice = 0
        self.disclosedQty = 0
        self.validity = 'DAY'
        self.offlineOrder = 'False'
        self.stopLoss = 0
        self.takeProfit = 0


    def setSymbole (self, symbol) :
        self.symbol =symbol

    def setqty (self, qty) :
        self.qty = qty 

    def setType (self, type) :
        self.type = type 
    
    def setside (self, side) :
        self.side = side 

    def setproductType (self, productType) :
        self.productType = productType 

    def setlimitPrice (self, limitPrice) :
        self.limitPrice = limitPrice 

    def setStopPrice (self, stopPrice) :
        self.stopPrice = stopPrice 

    def setTakeProfit (self, takeProfit) :
        self.takeProfit = takeProfit       

    def getJsonStructure (self) :
        return json.loads(json.dumps(self.__dict__))  

                             