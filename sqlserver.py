import pyodbc

class SqlServer:

    # Cadenas de conexión
    #'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
    #'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;

    def __init__(self, cnn_str):
        self.connection = pyodbc.connect(cnn_str)
        self.cursor = self.connection.cursor()

    def insert(self, table_name, data_dict):
        try:
            keys    = data_dict.keys()
            values  = tuple(data_dict.values())
            column_names = ",".join(keys)
            decorators   = ",".join(['?'] * len(keys))
            sql_str = "INSERT INTO {} ({}) values ({})".format(table_name, column_names, decorators)
            count = self.cursor.execute(sql_str,values).rowcount
            self.connection.commit()
            return count
        except Exception as e:
            print("Sucedió algo inesperado al insertar :: ", e)
        finally:
            self.connection.close()