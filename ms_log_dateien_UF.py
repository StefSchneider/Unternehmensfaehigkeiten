"""
Der Microservice verwaltet alle Log-Dateien und bestimmt, in welche Log-Dateien die Log-Daten geschrieben werden sollen.
Die Log-Dateien werden in einem eigenen Unterverzeichnis abgespeichert, Name und Pfad des Unterverzeichnisses werden
über die individuellen Configdaten eingelesen-
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
log_verzeichnis: str = ""
zeitstempel_url: str = ""



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
    _verwendete_microservices: list = config_daten_individuell_gesamt["verwendete_microservices"]
    _microservice_daten: dict = {}
    for _microservice in _verwendete_microservices:
        _microservice_daten[_microservice] = config_daten_allgemein_gesamt["microservices"][_microservice]
    global zeitstempel_url
    zeitstempel_url = "http://" \
                      + "localhost:" \
                      + str(_microservice_daten["zeitstempel"]["server_port"]) \
                      + _microservice_daten["zeitstempel"]["route"]
    global log_verzeichnis
    log_verzeichnis = config_daten_individuell_gesamt["log_verzeichnis"]

    return None

def log_verzeichnis_anlegen():
    if not pathlib.Path(log_verzeichnis).exists():
        pathlib.Path(log_verzeichnis).mkdir()

    return None

def periodische_log_dateien_auflisten() -> list:
    alle_log_dateien: list = os.listdir(log_verzeichnis)
    _alle_log_dateien_periodisch: list = []
    for _dateiname in alle_log_dateien:
        _log_datei_name: str = _dateiname.rsplit(".") # trennt das Suffix ab
        if re.match("log_datei_periodisch_[0-9]{14}", _log_datei_name[0]):
            _alle_log_dateien_periodisch.append(_dateiname)
            # nimmt nur Dateien auf, deren Name (ohne Suffix) der Namenskonvention entspricht

    return _alle_log_dateien_periodisch

def periodische_log_datei_bestimmen(zeitstempel_ein: str):
    _alle_log_dateien_periodisch = periodische_log_dateien_auflisten()
    _zeitstempel_aktuell = zeitstempel_ein
    _ziffern_zeitstempel_aktuell: list = re.findall(r"\d+", _zeitstempel_aktuell)[:-1]
    # filtert aus dem Zeitstempel die für die Namensbildung der Log-Datei erforderlichen Ziffern
    _ziffern_gesamt_zeitstempel_aktuell = "".join(_ziffern_zeitstempel_aktuell)
    if len(_alle_log_dateien_periodisch) == 0:
        _ziffern_zeitstempel_neueste_log_datei = ["0"]
    else:
        _neueste_log_datei_periodisch = max(_alle_log_dateien_periodisch)
        _ziffern_zeitstempel_neueste_log_datei: list = re.findall(r"\d+", _neueste_log_datei_periodisch)
    if int(_ziffern_gesamt_zeitstempel_aktuell) - int(_ziffern_zeitstempel_neueste_log_datei[0]) \
            >= config_daten_individuell_gesamt["log_dateien"]["periodisch"]["intervall"] * 100:
        # Faktor 100 berechnet Minuten aus der Intervall-Angabe
        periodische_log_datei_erzeugen(_ziffern_gesamt_zeitstempel_aktuell)
    while len(periodische_log_dateien_auflisten()) > config_daten_individuell_gesamt["log_dateien"]["periodisch"]["anzahl"]:
        _aelteste_log_datei_periodisch_name = min(periodische_log_dateien_auflisten())
        _aelteste_log_datei_periodisch = log_verzeichnis + _aelteste_log_datei_periodisch_name
        os.remove(_aelteste_log_datei_periodisch)
        # löscht alle periodischen Log-Dateien, deren Anzahl das Maximum übersteigen
    _log_datei_periodisch = max(periodische_log_dateien_auflisten()).split(".")[0]
    # verhindert doppeltes Anhängen von suffix

    return _log_datei_periodisch

def periodische_log_datei_erzeugen(zeitergaenzung: str):
    _log_datei_periodisch_name = config_daten_individuell_gesamt["log_dateien"]["periodisch"]["name"] + zeitergaenzung
    _log_datei_periodisch_neu = str(log_verzeichnis) \
                                + _log_datei_periodisch_name \
                                + "." \
                                + config_daten_individuell_gesamt["log_dateien"]["periodisch"]["suffix"]
#    _inhalt_log_datei_periodisch_neu: list = ["{\n", "}\n"] # bereitet die Log-Eintraege als json vor
    with open(_log_datei_periodisch_neu, mode = "w") as _log_datei_periodisch_neu_obj_aus:
        _log_datei_periodisch_neu_obj_aus.write("")
#        for _zeile in _inhalt_log_datei_periodisch_neu:
#            _log_datei_periodisch_neu_obj_aus.write(_zeile)

    return _log_datei_periodisch_neu


class Log_Dateien():

    def __init__(self):
        self._log_dateien_gesamt: dict = {}

    def hole_zusatzdaten(self): # Zeitstempel
        self._zeitstempel_anfrage = urllib.request.Request(url = zeitstempel_url, method = "GET")
        self.zeitstempel_daten = urllib.request.urlopen(self._zeitstempel_anfrage)
        self.zeitstempel_daten = json.load(self.zeitstempel_daten)

        return self.zeitstempel_daten

    def get(self, zeitstempel):
        self._log_datei_permanent = str(log_verzeichnis) \
                                    + config_daten_individuell_gesamt["log_dateien"]["permanent"]["name"] \
                                    + "." \
                                    + config_daten_individuell_gesamt["log_dateien"]["permanent"]["suffix"]
        self._log_datei_periodisch = str(log_verzeichnis) \
                                     + periodische_log_datei_bestimmen(zeitstempel) \
                                     + "." \
                                     + config_daten_individuell_gesamt["log_dateien"]["periodisch"]["suffix"]
        self._log_dateien_gesamt["log_datei_permanent"] = self._log_datei_permanent
        self._log_dateien_gesamt["log_datei_periodisch"] = self._log_datei_periodisch

        return self._log_dateien_gesamt

    def post(self):

        return "OK POST"

    def put(self):

        return "OK PUT"

    def delete(self):
        alle_log_dateien: list = os.listdir(log_verzeichnis)
        for _log_datei_name in alle_log_dateien:
            _log_datei: str = str(log_verzeichnis) + _log_datei_name
            os.remove(_log_datei)

        return "Log-Dateien gelöscht"


app = Flask(__name__)

@app.route("/log_dateien", methods = ["GET", "POST", "PUT", "DELETE"])
def ms_log_dateien() -> str:
    _log_dateien = Log_Dateien()
    _log_dateien._zusatzdaten_ein = _log_dateien.hole_zusatzdaten()
    _zeitstempel_UTC = _log_dateien._zusatzdaten_ein["zeitstempel_UTC"]
    _log_dateien_obj_aus: dict = {}
    if request.method == "GET":
        _log_dateien._log_dateien_gesamt = _log_dateien.get(_zeitstempel_UTC)
    elif request.method == "POST":
        _log_dateien._log_dateien_gesamt = _log_dateien.post()
    elif request.method == "PUT":
        _log_dateien._log_dateien_gesamt = _log_dateien.put()
    elif request.method == "DELETE":
        _log_dateien.delete()
        return "Log-Dateien gelöscht"
    _log_dateien_obj_aus["log_datei_permanent"] = _log_dateien._log_dateien_gesamt["log_datei_permanent"]
    _log_dateien_obj_aus["log_datei_periodisch"] = _log_dateien._log_dateien_gesamt["log_datei_periodisch"]

    return jsonify(_log_dateien_obj_aus)


if __name__ == "__main__":
    _log_dateien_config_daten_ein = lade_configdaten()
    verteile_configdaten(_log_dateien_config_daten_ein)
    log_verzeichnis_anlegen()
    app.run(port = server_port, debug = True)