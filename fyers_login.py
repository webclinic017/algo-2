from fyers_api import accessToken
from fyers_api import fyersModel 
import requests
app_id = "50S5CYV54O"
app_secret = "XD18O1TC04"  

def getLoginHtml():
    app_session = accessToken.SessionModel(app_id, app_secret) 
    response = app_session.auth()
    authorization_code = response['data']['authorization_code']
    app_session.set_token(authorization_code)
    url =app_session.generate_token()
    return requests.get(url).text