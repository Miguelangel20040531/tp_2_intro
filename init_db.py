import mysql.connector

# Si ejecutan este script van a poder crear la base de datos y las tablas necesarias para el proyecto. Solo necesitan tener MySQL instalado y el usuario root con contraseña root (o modificar el script para usar otro usuario/contraseña).

with open("init_db.sql") as f:
    sql = f.read()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Statement executed")

cursor.close()
conn.close()