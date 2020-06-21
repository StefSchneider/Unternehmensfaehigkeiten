"""
Der Microservice errechnet ein Ergebnis auf Basis der mitgelieferten JSON-Daten für programm_nummer, nummer_1 und
nummer_2. Zurückgeliefert werden neben den Rechendaten auch ein Zeitstempel, eine ID und ein Status-Code. Diese Daten
sollen für die Einträge in die Log-Dateien verwendet werden.
"""

from flask import Flask, request, jsonify
import argparse
import pathlib
import urllib
import sys
import json

server_port: int = 0
config_daten_individuell_gesamt: dict = {}
config_daten_allgemein_gesamt: dict = {}
ID_url: str = ""


def lade_configdaten() -> dict:
    global server_port
    _parser = argparse.ArgumentParser(description = "Daten für individuelle Configdatei")
    _parser.add_argument("--config_datei_allgemein", type = str, help = "Name der allgemeinen Configdatei inkl. Pfad")
    _parser.add_argument("--config_datei_individuell", type = str, help = "Name der individuellen Configdatei inkl. Pfad")
    _parser.add_argument("--server_port", type = int, default = 80, help = "Nummer des anzusprechenden Ports")
    _config_daten_ein = _parser.parse_args()
    _config_datei_allgemein_ein = _config_daten_ein.config_datei_allgemein
    _config_datei_allgemein_ein = pathlib.Path(_config_datei_allgemein_ein)
    _config_datei_individuell_ein = _config_daten_ein.config_datei_individuell
    _config_datei_individuell_ein = pathlib.Path(_config_datei_individuell_ein)
    server_port = _config_daten_ein.server_port
    with open(_config_datei_individuell_ein, mode = "r") as _config_datei_individuell_obj_ein:
        _config_daten_individuell_gesamt = json.load(_config_datei_individuell_obj_ein)
    with open(_config_datei_allgemein_ein, mode = "r") as _config_datei_allgemein_obj_ein:
        _config_daten_allgemein_gesamt = json.load((_config_datei_allgemein_obj_ein))
    _config_daten_gesamt: dict = {}
    _config_daten_gesamt["config_daten_allgemein_gesamt"] = _config_daten_allgemein_gesamt
    _config_daten_gesamt["config_daten_individuell_gesamt"] = _config_daten_individuell_gesamt

    return _config_daten_gesamt

def verteile_configdaten(config_daten_ein: dict):
    _config_daten_gesamt_ein = config_daten_ein
    global config_daten_individuell_gesamt
    global config_daten_allgemein_gesamt
    config_daten_individuell_gesamt = _config_daten_gesamt_ein["config_daten_individuell_gesamt"]["config_datei_individuell"]
    config_daten_allgemein_gesamt = _config_daten_gesamt_ein["config_daten_allgemein_gesamt"]["config_daten_allgemein"]
    # Ab hier Verteilung der individuellen Configdaten für den Microservice
    global ID_url
    _verwendete_microservices: list = config_daten_individuell_gesamt["verwendete_microservices"]
    _microservice_daten: dict = {}
    for microservice in _verwendete_microservices:
        _microservice_daten[microservice] = config_daten_allgemein_gesamt["microservices"][microservice]
    ID_url = "http://" \
             + "localhost:" \
             + str(_microservice_daten["ID"]["server_port"]) \
             + _microservice_daten["ID"]["route"]

    return None


class Ergebnis():

    def __init__(self):
        self._programm_nummer: int = 0
        self._nummer_1: int = 0
        self._nummer_2: int = 0
        self._ergebnis: int = 0
        self._zeitstempel: str = ""
        self._ID: str = ""
        self._zusatzdaten_ein: dict = {}
        self._ergebnis_daten: str = ""

    def hole_zusatzdaten(self): # ID
        self._ID_anfrage = urllib.request.Request(url = ID_url, method = "GET")
        self._ID_daten = urllib.request.urlopen(self._ID_anfrage)
        self._ID_daten = json.load(self._ID_daten)

        return self._ID_daten

    def get(self):
        if self._programm_nummer % 3 == 1:
            self._ergebnis: int = self._nummer_1 + self._nummer_2
        elif self._programm_nummer % 3 == 2:
            self._ergebnis = self._nummer_1 * self._nummer_2
        elif self._programm_nummer % 3 == 0:
            try:
                self._ergebnis = self._nummer_1 // self._nummer_2
            except ZeroDivisionError:
                self._ergebnis = 1
        else:
            self._ergebnis = self._nummer_1 - self._nummer_2

        return self._ergebnis

    def post(self):

        return "OK POST"

    def put(self):

        return "OK PUT"

    def delete(self):

        return "OK DELETE"


class Ergebnis():

    def __init__(self):
        self._programm_nummer: int = 0
        self._nummer_1: int = 0
        self._nummer_2: int = 0
        self._ergebnis: int = 0
        self._zeitstempel: str = ""
        self._ID: str = ""
        self._zusatzdaten_ein: dict = {}
        self._ergebnis_daten: str = ""

    def hole_zusatzdaten(self): # ID
        self._ID_anfrage = urllib.request.Request(url = ID_url, method = "GET")
        self._ID_daten = urllib.request.urlopen(self._ID_anfrage)
        self._ID_daten = json.load(self._ID_daten)

        return self._ID_daten

    def get(self):
        if self._programm_nummer % 3 == 1:
            self._ergebnis: int = self._nummer_1 + self._nummer_2
        elif self._programm_nummer % 3 == 2:
            self._ergebnis = self._nummer_1 * self._nummer_2
        elif self._programm_nummer % 3 == 0:
            try:
                self._ergebnis = self._nummer_1 // self._nummer_2
            except ZeroDivisionError:
                self._ergebnis = 1
        else:
            self._ergebnis = self._nummer_1 - self._nummer_2

        return self._ergebnis

    def post(self):

        return "OK POST"

    def put(self):

        return "OK PUT"

    def delete(self):

        return "OK DELETE"

app = Flask(__name__)

@app.route("/rechenoperation", methods = ["GET", "POST", "PUT", "DELETE"])
def ms_rechenoperation():
    _ergebnis = Ergebnis()
    _ergebnis._ergebnis_daten = request.get_json()
    if _ergebnis._ergebnis_daten == None: # Fallback-Daten, falls keine JSON-Daten übermittelt werden
        _ergebnis._programm_nummer = -1
        _ergebnis._nummer_1 = -1
        _ergebnis._nummer_2 = -1
    else:
        _ergebnis._programm_nummer = _ergebnis._ergebnis_daten["programm_nummer"]
        _ergebnis._nummer_1 = _ergebnis._ergebnis_daten["nummer_1"]
        _ergebnis._nummer_2 = _ergebnis._ergebnis_daten["nummer_2"]
    _ergebnis._zusatzdaten = _ergebnis.hole_zusatzdaten()
    _ergebnis_obj_aus: dict = {}
    _ergebnis_obj_aus["zeitstempel"] = _ergebnis._zusatzdaten["zeitstempel"]
    _ergebnis_obj_aus["ID"] = _ergebnis._zusatzdaten["ID"]
    _ergebnis_obj_aus["name_microservice"] = sys._getframe(0).f_code.co_name
    if request.method == "GET":
        _rechenergebnis = _ergebnis.get()
    elif request.method == "POST":
        _rechenergebnis = _ergebnis.post()
    elif request.method == "PUT":
        _rechenergebnis = _ergebnis.put()
    elif request.method == "DELETE":
        _rechenergebnis = _ergebnis.delete()
    _ergebnis_obj_aus["daten_microservice"] = [
        {"programm_nummer": _ergebnis._programm_nummer},
        {"nummer_1": _ergebnis._nummer_1},
        {"nummber_2": _ergebnis._nummer_2},
        {"ergebnis": _rechenergebnis},
#        {"status_code": -1}
    ]

    return jsonify(_ergebnis_obj_aus)


if __name__ == "__main__":
    _rechenoperation_config_daten_ein = lade_configdaten()
    verteile_configdaten(_rechenoperation_config_daten_ein)
    app.run(port = server_port, debug = True)