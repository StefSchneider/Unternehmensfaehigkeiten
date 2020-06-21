"""
Der Miroservice erstellt eine ID auf Basis des Zeitstempels. Werden für die Log-Daten die Microservices "Zeitstempel"
und "ID" nacheinander aufgerufen, ensteht eine Differenz zwischen dem originären und dem für die ID verwendeten
Zeitstempel. Um dies zu vermeiden, überträgt die ID auch ihren zugehoerigen Zeitstempel mit.
"""

from flask import Flask, request, jsonify
import urllib
import argparse
import pathlib
import json
import os

server_port: int = 0
config_daten_individuell_gesamt: dict = {}
config_daten_allgemein_gesamt: dict = {}
microservice_urls: dict = {}
zeitstempel_url: str = ""


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
    global zeitstempel_url
    _verwendete_microservices: list = config_daten_individuell_gesamt["verwendete_microservices"]
    _microservice_daten: dict = {}
    for microservice in _verwendete_microservices:
        _microservice_daten[microservice] = config_daten_allgemein_gesamt["microservices"][microservice]
    zeitstempel_url = "http://" \
                      + "localhost:" \
                      + str(_microservice_daten["zeitstempel"]["server_port"]) \
                      + _microservice_daten["zeitstempel"]["route"]

    return None


class ID:

    def __init__(self):
        self._ID: str = ""
        self._zeitstempel_lokal: str = ""
        self._zeitstempel_UTC: str = ""
        self._zusatzdaten_ein: dict = {}

    def hole_zusatzdaten(self): # Zeitstempel
        self._zeitstempel_anfrage = urllib.request.Request(url = zeitstempel_url, method = "GET")
        self._zeitstempel_daten = urllib.request.urlopen(self._zeitstempel_anfrage)
        self._zeitstempel_daten = json.load(self._zeitstempel_daten)

        return self._zeitstempel_daten

    def get(self, zeitstempel_UTC_ein): # build ID with UTC-timestamp
        self._zeitstempel_UTC = zeitstempel_UTC_ein
        self._zeitstempel_UTC = self._zeitstempel_UTC.split(" ") # trenne Datumsteil und Zeitteil, ignoriere UTC-Teil
        self._operating_system_ID: int = os.getpid()
        self._ID = str(self._operating_system_ID) \
              + "_" \
              + self._zeitstempel_UTC[0] \
              + "_" \
              + self._zeitstempel_UTC[1]

        return self._ID

    def post(self):
        self._ID = "ID"

        return "OK POST"

    def put(self):
        self._ID = "00000000"

        return "OK PUT"

    def delete(self):
        self._ID = "OK"

        return "OK DELETE"


app = Flask(__name__)

@app.route("/ID", methods = ["GET", "POST", "PUT", "DELETE"])
def ms_ID() -> str:
    _ID = ID()
    _ID._zusatzdaten_ein = _ID.hole_zusatzdaten()
    _ID_obj_aus: dict = {}
    if request.method == "GET":
        _ID._ID = _ID.get(_ID._zusatzdaten_ein["zeitstempel_UTC"])
    elif request.method == "POST":
        _ID._ID = _ID.post()
    elif request.method == "PUT":
        _ID._ID = _ID.put()
    elif request.method == "DELETE":
        _ID._ID = _ID.delete()
    _ID_obj_aus["zeitstempel"] = _ID._zusatzdaten_ein["zeitstempel_lokal"]
    _ID_obj_aus["ID"] = _ID._ID

    return jsonify(_ID_obj_aus)


if __name__ == "__main__":
    _ID_config_daten_ein = lade_configdaten()
    verteile_configdaten(_ID_config_daten_ein)
    app.run(port = server_port, debug = True)