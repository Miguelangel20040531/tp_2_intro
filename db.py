import mysql.connector
# Esto modifiquenlo segun el usuario y contraseña que tengan en su MySQL.

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="miguel",
        password="1234",
        database="ids_sqd"
    )