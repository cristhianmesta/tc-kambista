import time
from datetime import datetime
import requests
from sqlserver import *


SQL_SERVER  = 'CM3-THINKPAD' 
SQL_DATABASE = 'TIPO_CAMBIO' 
SQL_USERNAME = '' 
SQL_PASSWORD = '' 

sql_cnn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER='+SQL_SERVER+';'
        r'DATABASE='+SQL_DATABASE+';'
        r'Trusted_Connection=yes;'
)

precio_venta_anterior   = 0
precio_venta            = 0

while True:
    resp = requests.get('https://api.kambista.com/v1/exchange/calculates?originCurrency=USD&destinationCurrency=PEN&amount=8&active=R')
    moment = datetime.now()
    
    if resp.status_code==200:

        try:
            data = resp.json()
            
            precio_compra = data['tc']['bid']
            precio_venta  = data['tc']['ask']
            

            icon = "🟡"

            if precio_venta > precio_venta_anterior and precio_venta_anterior != 0: icon = "🔴"
            if precio_venta < precio_venta_anterior and precio_venta_anterior != 0: icon = "🟢"

            precio_venta_anterior = precio_venta

            print(moment, '\t', precio_compra, '\t', precio_venta, icon)

            db = SqlServer(sql_cnn_str)
            db.insert('TIPO_CAMBIO_KAMBISTA',{'Fecha' : moment, 'Compra' : precio_compra, 'Venta': precio_venta })

        except:
            print("No se pudieron recuperar los datos")

    time.sleep(20) 


# from bs4 import BeautifulSoup
# r = requests.get('https://kambista.com/')
# # soup = BeautifulSoup(r.text, "html.parser")
# # time.sleep(3)
# # precio_compra = soup.find("strong", {"id": "valcompra"}).text.strip()
# # precio_venta = soup.find("strong", {"id": "valventa"}).text.strip()
# # while True:
# #     print(precio_compra)
# #     print(precio_venta)
# #     print("-------------")
# #     time.sleep(3) 