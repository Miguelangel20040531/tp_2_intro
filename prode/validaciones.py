from datetime import datetime

def es_texto_no_vacio(texto):
    return isinstance(texto, str) and texto.strip() != ""

def es_email_basico(email):
    return isinstance(email, str) and "@" in email and "." in email and email.strip() != ""

def tiene_formato_string(cadena):
    """ Valido que sea string y que no sea string vacio"""
    return isinstance(cadena, str) and cadena.strip() != "" and cadena.isalpha()

def es_entero(goles):
    try:
        int(goles)
        return True
    except ValueError:
        return False

def es_fecha_correcta(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def es_positivo(numero):
    return numero>=0
