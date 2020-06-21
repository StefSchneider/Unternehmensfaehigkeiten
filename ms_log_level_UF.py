"""
Der Microservice verwaltet die Datei, in der die Haeufigkeit der Aufrufe je Microservice erfasst wird und errechnet aus
den Einträgen, ob der jeweilige Microservice erfasst wird oder nicht. Soll er erfasst werden, ist der Rückgabewert "ja",
ansonsten ist er "nein". Damit wird die Erfassung in der permanenten Log-Datei gesteuert, eine Erfassung in der
aktuellen periodischen Log-Datei erfolgt sowieso immer.
"""

from flask import Flask, request, jsonify
import argparse
import pathlib
import urllib
import re
import json
import os

server_port: int = 0
config_daten_individuell_gesamt: dict = {}
config_daten_allgemein_gesamt: dict = {}
log_level: dict ={}



def lade_configdaten() -> dict:
    _parser = argparse.ArgumentParser(description = "Daten für individuelle Configdatei")
    _parser.add_argument("--config_datei_allgemein", type = str, help = "Name der allgemeinen Configdatei inkl. Pfad")
    _parser.add_argument("--config_datei_individuell", type = str, help = "Name der individuellen Configdatei inkl. Pfad")
    _parser.add_argument("--server_port", type = int, default = 80, help = "Nummer des anzusprechenden Ports")
    config_daten_ein = _parser.parse_args()
    config_datei_allgemein_ein = config_daten_ein.config_datei_allgemein
    config_datei_allgemein_ein = pathlib.Path(config_datei_allgemein_ein)
    config_datei_individuell_ein = config_daten_ein.config_datei_individuell
    _config_datei_individuell_ein = pathlib.Path(config_datei_individuell_ein)
    global server_port
    server_port = config_daten_ein.server_port
    with open(_config_datei_individuell_ein, mode = "r") as _config_datei_individuell_obj_ein:
        config_daten_individuell_gesamt = json.load(_config_datei_individuell_obj_ein)
    with open(config_datei_allgemein_ein, mode ="r") as _config_datei_allgemein_obj_ein:
        config_daten_allgemein_gesamt = json.load((_config_datei_allgemein_obj_ein))
    _config_daten_gesamt: dict = {}
    _config_daten_gesamt["config_daten_allgemein_gesamt"] = config_daten_allgemein_gesamt
    _config_daten_gesamt["config_daten_individuell_gesamt"] = config_daten_individuell_gesamt

    return _config_daten_gesamt

def verteile_configdaten(config_daten_ein: dict):
    _config_daten_gesamt_ein = config_daten_ein
    global config_daten_individuell_gesamt
    config_daten_individuell_gesamt = _config_daten_gesamt_ein["config_daten_individuell_gesamt"]["config_datei_individuell"]
    global config_daten_allgemein_gesamt
    config_daten_allgemein_gesamt = _config_daten_gesamt_ein["config_daten_allgemein_gesamt"]["config_daten_allgemein"]
    # Ab hier Verteilung der individuellen Configdaten für den Microservice
    global log_level
    log_level = config_daten_individuell_gesamt["log_level"]

    return None

def lade_log_level() -> dict:
    log_level_daten: dict = {}
    log_level_datei: str = config_daten_individuell_gesamt["log_level_datei"]["pfad"] \
                           + config_daten_individuell_gesamt["log_level_datei"]["datei"] \
                           + "." \
                           + config_daten_individuell_gesamt["log_level_datei"]["suffix"]
    try:
        with open(log_level_datei, mode = "r") as _log_level_datei_obj_ein:
            log_level_daten = json.load(_log_level_datei_obj_ein)
    except FileNotFoundError:
        pass

    return log_level_daten

def speichere_log_level(log_level_daten_ein: dict):
    log_level_datei: str = config_daten_individuell_gesamt["log_level_datei"]["pfad"] \
                           + config_daten_individuell_gesamt["log_level_datei"]["datei"] \
                           + "." \
                           + config_daten_individuell_gesamt["log_level_datei"]["suffix"]
    with open(log_level_datei, mode = "w") as _log_level_datei_obj_aus:
        json.dump(log_level_daten_ein, _log_level_datei_obj_aus)

    return None



class Log_Level:

    def __init__(self):
        self._name_microservice: str = ""
        self._log_level_freigabe: bool = False

    def get(self, name_microservice: str):
        _log_level_daten_gesamt: dict = {}
        _log_level_freigabe: bool = False
        name_microservice = name_microservice.split("_", 1)[1]
        config_datei_daten = config_daten_allgemein_gesamt["microservices"][name_microservice]["config_datei_individuell"]
        _config_datei_individuell = config_datei_daten["pfad"] \
                                    + config_datei_daten["datei"] \
                                    + "." \
                                    + config_datei_daten["suffix"]
        with open(_config_datei_individuell, mode = "r") as _config_datei_individuell_obj_ein:
            _config_datei_individuell_daten = json.load(_config_datei_individuell_obj_ein)
        kernservice_daten = _config_datei_individuell_daten["config_datei_individuell"]["kernservice"]
        if kernservice_daten.upper() == "JA":
            _log_level_freigabe = True
        elif kernservice_daten.upper() == "NIE":
            _log_level_microservice = "nie"
        else:
            _log_level_berechnungen: list = []
            _log_level_daten_gesamt = lade_log_level()
            try:
                _log_level_daten_microservice = int(_log_level_daten_gesamt[name_microservice]) + 1 # Erhöhung durch aktuellen Aufruf
            except KeyError:
                _log_level_daten_microservice = 1 # Neueintrag für Microservice
            for _log_level_schluessel in config_daten_individuell_gesamt["log_level"]:
                if _log_level_schluessel.upper() != "KERNSERVICE" and _log_level_schluessel.upper() != "NIE":
                    _log_level_berechnungen.append(_log_level_daten_microservice % config_daten_individuell_gesamt["log_level"][_log_level_schluessel])
            print(_log_level_berechnungen)
            if min(_log_level_berechnungen) == 0:
                _log_level_freigabe = True
        _log_level_daten_gesamt[name_microservice] = _log_level_daten_microservice
        speichere_log_level(_log_level_daten_gesamt)

        return _log_level_freigabe

    def post(self):

        return "OKAY POST"

    def put(self):

        return "OK PUT"

    def delete(self):

        return "OK DELETE"


app = Flask(__name__)

@app.route("/log_level", methods = ["GET", "POST", "PUT", "DELETE"])
def ms_log_level():
    _log_level = Log_Level
    _log_level._name_microservice = request.get_json()
    if request.method == "GET":
        _log_level._log_level_freigabe = _log_level.get(_log_level._name_microservice, _log_level._name_microservice)
    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        # Leere die Log-Datei
        pass

    return jsonify(_log_level._log_level_freigabe)


if __name__ == "__main__":
    _log_level_config_daten_ein = lade_configdaten()
    verteile_configdaten(_log_level_config_daten_ein)
    app.run(port = server_port, debug = True)