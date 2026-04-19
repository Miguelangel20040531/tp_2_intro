import mysql.connector
# Esto modifiquenlo segun el usuario y contraseña que tengan en su MySQL.

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="miguel",
        password="1234",
        database="mundial" # Se cambió esta linea a "mundial" (antes "ids_sqd"), para que coincida con la base que se crea en init_db.sql.
    )
