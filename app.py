from flask import Flask
from partidos import partidos_db
from usuarios import usuarios_db
from ranking import ranking_bp

app= Flask(__name__)

app.register_blueprint(partidos_db, url_prefix="/partidos")
app.register_blueprint(usuarios_db, url_prefix="/usuarios")
app.register_blueprint(ranking_bp, url_prefix='/ranking')





if __name__== "__main__":
    app.run(port=5000,debug=True)
