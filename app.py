from flask import Flask
from partidos import partidos_db
from usuarios import usuarios_db
from db import get_connection

app = Flask(__name__)

app.register_blueprint(partidos_db, url_prefix="/partidos")
app.register_blueprint(usuarios_db, url_prefix="/usuarios")

@app.route("/")
def home():
    return " Mundial 2026 "

if __name__ == "__main__":
    app.run(debug=True)
