import time
from datetime import datetime
import requests
from sqlserver import *


SERVICIOS = (
    { 
        "PORTAL"    : "KAMBISTA", 
        "URL"       : "https://api.kambista.com/v1/exchange/calculates?originCurrency=USD&destinationCurrency=PEN&amount=8&active=R",
        "METODO"    : "GET"
    },
    { 
        "PORTAL"    : "REXTIE", 
        "URL"       : "https://app.rextie.com/api/v1/fxrates/rate/?origin=template-original&utm_source=search,adwords&utm_medium=cpc,ppc&utm_id=brand&utm_term=brand,rextie&utm_content=performance&utm_campaign=performance_aon_brand_registros_search&hsa_acc=5383902905&hsa_cam=14396964907&hsa_grp=125801717509&hsa_ad=541122542085&hsa_src=g&hsa_tgt=kwd-321924773704&hsa_kw=rextie&hsa_mt=b&hsa_net=adwords&hsa_ver=3&gclid=cjwkcajwquwvbhbreiwat1kmwi5_rmmlhvedqxfofgsscudi9ca-loipezxlzih6o4olwwed_3tsmroc88eqavd_bwe",
        "METODO"    : "POST"
    },
    { 
        "PORTAL"    : "TKAMBIO", 
        "URL"       : "https://tkambio.com/wp-admin/admin-ajax.php?action=get_exchange_rate",
        "METODO"    : "GET"
    }
)

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
precio_compra_anterior  = {"KAMBISTA": 0, "REXTIE": 0, "TKAMBIO": 0}
precio_compra           = 0

precio_venta_anterior   = {"KAMBISTA": 0, "REXTIE": 0, "TKAMBIO": 0}
precio_venta            = 0

while True:

    for servicio in SERVICIOS:

        resp = requests.request(servicio["METODO"],servicio["URL"])
        moment = datetime.now()
        
        if resp.status_code==200 or resp.status_code==201:

            try:
                data = resp.json()

                if servicio["PORTAL"] == "KAMBISTA":
                    precio_compra = float(data['tc']['bid'])
                    precio_venta  = float(data['tc']['ask'])
                
                if servicio["PORTAL"] == "REXTIE":
                    precio_compra = float(data['fx_rate_buy'])
                    precio_venta  = float(data['fx_rate_sell'])
                    
                if servicio["PORTAL"] == "TKAMBIO":
                    precio_compra = float(data['buying_rate'])
                    precio_venta  = float(data['selling_rate'])
                
                icon_pc = "🟡"
                pc_anterior = float(precio_compra_anterior[servicio["PORTAL"]])
         
                
                if precio_compra>pc_anterior and pc_anterior!=0: icon_pc = "🔴"
                if precio_compra<pc_anterior and pc_anterior!=0: icon_pc = "🟢"
              
                precio_compra_anterior[servicio["PORTAL"]] = precio_compra


                icon_pv = "🟡"
                pv_anterior = float(precio_venta_anterior[servicio["PORTAL"]])

                if precio_venta > pv_anterior and pv_anterior!=0: icon_pv = "🔴"
                if precio_venta < pv_anterior and pv_anterior!=0: icon_pv = "🟢"

                precio_venta_anterior[servicio["PORTAL"]] = precio_venta

                print(moment,'\t', servicio["PORTAL"],'\t', precio_compra, icon_pc,'\t', precio_venta, icon_pv)

                db = SqlServer(sql_cnn_str)
                db.insert('TIPO_CAMBIO_'+servicio["PORTAL"],{'Fecha' : moment, 'Compra' : precio_compra, 'Venta': precio_venta })

            except:
                print("No se pudieron recuperar los datos")

    time.sleep(20) 