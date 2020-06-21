from flask import Flask, jsonify
import urllib
import urllib.request
import pathlib
import random
import json
import subprocess


CONFIG_DATEI_ALLGEMEIN: dict = {"pfad": r"C:\Users\schne\Coding\Python\Projects\Unternehmensfaehigkeiten\\",
                                 "name": "unternehmensfaehigkeiten_configdaten_allgemein",
                                 "suffix": "cfg"
                                 }

server_port: int = 80
config_datei_allgemein_ein: str = CONFIG_DATEI_ALLGEMEIN["pfad"] \
                                  + CONFIG_DATEI_ALLGEMEIN["name"] \
                                  + "." \
                                  + CONFIG_DATEI_ALLGEMEIN["suffix"]
config_daten_individuell_gesamt: dict = {}
config_daten_microservices: dict = {}


def lade_configdaten() -> dict:
    _config_datei_ein = pathlib.Path(config_datei_allgemein_ein)
    with open(_config_datei_ein, mode = "r") as _config_datei_obj_ein:
        _config_daten_gesamt = json.load(_config_datei_obj_ein)

    return _config_daten_gesamt

def starte_microservices(config_daten_microservices_ein: dict):
    for microservice in config_daten_microservices_ein:
        kommandos: list = ["python.exe"]
        _microservice_skript = config_daten_microservices_ein[microservice]["microservice_skript"]["pfad"] \
                        + config_daten_microservices_ein[microservice]["microservice_skript"]["datei"]\
                        + "."\
                        + config_daten_microservices_ein[microservice]["microservice_skript"]["suffix"] \
                        + " "
        _config_datei_individuell = config_daten_microservices_ein[microservice]["config_datei_individuell"]["pfad"] \
                                    + config_daten_microservices_ein[microservice]["config_datei_individuell"]["datei"]\
                                    + "." \
                                    + config_daten_microservices_ein[microservice]["config_datei_individuell"]["suffix"]\
                                    + " "
        _server_port = config_daten_microservices_ein[microservice]["server_port"]
        kommandos.extend([_microservice_skript,
                          "--config_datei_allgemein", config_datei_allgemein_ein,
                          "--config_datei_individuell", _config_datei_individuell,
                          "--server_port", str(_server_port)])
        subprocess.Popen(kommandos, shell=True)

    return None

def logging(log_daten_ein: dict):
    # log-level den Namen des Microservice aus log_daten_ein mitgeben
    _log_daten_gesamt = json.dumps(log_daten_ein).encode("utf-8")
#    print(_log_daten_gesamt)
    _logging_url = "http://localhost:" \
                   + str(config_daten_microservices["logging"]["server_port"]) \
                   + config_daten_microservices["logging"]["route"]
    _logging_buchung = urllib.request.Request(url = _logging_url, method = "POST")
    _logging_buchung.add_header('Content-Type', "application/json; charset=utf-8")
    _logging_buchung.add_header('Content-Length', len(_log_daten_gesamt))
    _logging_daten = urllib.request.urlopen(_logging_buchung, _log_daten_gesamt)


    return None


app = Flask(__name__)

@app.route("/")
def index():
    _verfuegbare_inhalte: str = "Verfügbare Inhalte: "
    for microservice in config_daten_microservices:
        _verfuegbare_inhalte += "".join((config_daten_microservices[microservice]["name"], ": ",
                                         config_daten_microservices[microservice]["route"], " | "))

    return _verfuegbare_inhalte


@app.route("/zeitstempel", methods = ["GET", "POST", "PUT", "DELETE"])
def ms_zeitstempel():
    _zeitstempel_url = "http://localhost:" \
                       + str(config_daten_microservices["zeitstempel"]["server_port"]) \
                       + config_daten_microservices["zeitstempel"]["route"]
    _zeitstempel_anfrage = urllib.request.Request(url = _zeitstempel_url, method = "GET")
    _zeitstempel_daten = urllib.request.urlopen(_zeitstempel_anfrage)
    _zeitstempel = _zeitstempel_daten.read().decode('utf-8')
#    logging(_zeitstempel)

    return _zeitstempel


@app.route("/ID")
def ms_ID():
    _ID_url = "http://localhost:" \
                       + str(config_daten_microservices["ID"]["server_port"]) \
                       + config_daten_microservices["ID"]["route"]
    _ID_anfrage = urllib.request.Request(url = _ID_url, method = "GET")
    _ID_daten = urllib.request.urlopen(_ID_anfrage)
    _ID = _ID_daten.read().decode('utf-8')

    return _ID


@app.route("/rechenoperation")
def ms_rechenoperation():
    _programm_nummer: int = random.randint(1, 4)
    _nummer_1: int = random.randint(0, 100)
    _nummer_2: int = random.randint(0, 100)
    _rechendaten_aus: dict = {}
    _rechendaten_aus["programm_nummer"] = _programm_nummer
    _rechendaten_aus["nummer_1"] = _nummer_1
    _rechendaten_aus["nummer_2"] = _nummer_2
    _rechendaten_aus = json.dumps(_rechendaten_aus).encode("utf-8")
    _rechenoperation_url = "http://localhost:" \
                       + str(config_daten_microservices["rechenoperation"]["server_port"]) \
                       + config_daten_microservices["rechenoperation"]["route"]
    _rechenoperation_anfrage = urllib.request.Request(url = _rechenoperation_url, method = "GET")
    _rechenoperation_anfrage.add_header('Content-Type', "application/json; charset=utf-8")
    _rechenoperation_anfrage.add_header('Content-Length', len(_rechendaten_aus))
    _rechenoperation_daten = urllib.request.urlopen(_rechenoperation_anfrage, _rechendaten_aus)
    _rechenoperation_status_code = urllib.request.urlopen(_rechenoperation_anfrage).getcode()
    _ergebnis = _rechenoperation_daten.read().decode('utf-8')
    _ergebnis = json.loads(_ergebnis)
    _ergebnis["status_code"] = _rechenoperation_status_code
    logging(_ergebnis)

    return jsonify(_ergebnis)

@app.route("/log_dateien", methods = ["GET", "DELETE"])
def ms_log_dateien():
    _log_dateien_url = "http://localhost:" \
                       + str(config_daten_microservices["log_dateien"]["server_port"]) \
                       + config_daten_microservices["log_dateien"]["route"]
    _log_dateien_anfrage = urllib.request.Request(url = _log_dateien_url, method = "DELETE")
    _log_dateien_daten = urllib.request.urlopen(_log_dateien_anfrage)
    _log_dateien_daten = _log_dateien_daten.read().decode('utf-8')

    return (_log_dateien_daten)




if __name__ == "__main__":
    config_daten_individuell_gesamt = lade_configdaten()
    config_daten_microservices = config_daten_individuell_gesamt["config_daten_allgemein"]["microservices"]
    starte_microservices(config_daten_microservices)
    app.run(port = server_port, debug = True)