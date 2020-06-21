"""
Der Microservice erstellt einen Zeitstempel auf Basis der aktuellen Zeit und einen Zeitstempel auf Basis der UTC-Zeit.
Die Daten werden in Form eines JSON zurückgegeben.
"""

from flask import Flask, request, jsonify
import argparse
import pathlib
import json
import datetime

server_port: int = 0
config_daten_individuell_gesamt: dict = {}


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

    return None


class Zeitstempel:

    def __init__(self):
        self._zeitstempel_lokal: str = ""
        self._zeitstempel_UTC: str = ""
        self._zeitstempel_daten: dict = {}

    def get(self):
        self._zeitstempel_UTC = datetime.datetime.now(datetime.timezone.utc)
        self._zeitstempel_lokal = self._zeitstempel_UTC.replace(tzinfo = datetime.timezone.utc)
        self._zeitstempel_lokal = self._zeitstempel_lokal.astimezone(tz = None)
        self._zeitstempel_lokal = self._zeitstempel_lokal.strftime("%Y-%m-%d %H:%M:%S %z")
        self._zeitstempel_UTC = self._zeitstempel_UTC.strftime("%Y-%m-%d %H:%M:%S %z")
        self._zeitstempel_daten["zeitstempel_lokal"] = self._zeitstempel_lokal
        self._zeitstempel_daten["zeitstempel_UTC"] = self._zeitstempel_UTC

        return self._zeitstempel_daten

    def post(self):
        self._zeitstempel_lokal = "ZEITSTEMPEL LOKAL"
        self._zeitstempel_UTC = "ZEITSTEMPEL UTC"
        self._zeitstempel_daten["zeitstempel_lokal"] = self._zeitstempel_lokal
        self._zeitstempel_daten["zeitstempel_UTC"] = self._zeitstempel_UTC

        return self._zeitstempel_daten

    def put(self):
        self._zeitstempel_lokal = "0000:00:00 00:00:00"
        self._zeitstempel_UTC = "0000:00:00 00:00:00"
        self._zeitstempel_daten["zeitstempel_lokal"] = self._zeitstempel_lokal
        self._zeitstempel_daten["zeitstempel_UTC"] = self._zeitstempel_UTC

        return self._zeitstempel_daten

    def delete(self):
        self._zeitstempel_lokal = "OK Lokal"
        self._zeitstempel_UTC = "OK UTC"
        self._zeitstempel_daten["zeitstempel_lokal"] = self._zeitstempel_lokal
        self._zeitstempel_daten["zeitstempel_UTC"] = self._zeitstempel_UTC

        return self._zeitstempel_daten

app = Flask(__name__)


@app.route("/zeitstempel", methods = ["GET", "POST", "PUT", "DELETE"])
def ms_zeitstempel() -> str:
    _zeitstempel = Zeitstempel()
    _zeitstempel_obj_aus: dict = {}
    if request.method == "GET":
        _zeitstempel = _zeitstempel.get()
    elif request.method == "POST":
        _zeitstempel = _zeitstempel.post()
    elif request.method == "PUT":
        _zeitstempel = _zeitstempel.put()
    elif request.method == "DELETE":
        _zeitstempel = _zeitstempel.delete()
    _zeitstempel_obj_aus["zeitstempel_lokal"] = _zeitstempel["zeitstempel_lokal"]
    _zeitstempel_obj_aus["zeitstempel_UTC"] = _zeitstempel["zeitstempel_UTC"]

    return jsonify(_zeitstempel_obj_aus)


if __name__ == "__main__":
    _zeitstempel_config_daten_ein = lade_configdaten()
    verteile_configdaten(_zeitstempel_config_daten_ein)
    app.run(port = server_port, debug = True)