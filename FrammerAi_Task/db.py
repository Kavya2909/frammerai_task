import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',  
        password='Qwerty@123', 
        database='crud_db'  
    )
