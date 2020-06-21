""""

"""

from flask import Flask, request, jsonify
import argparse
import pathlib
import urllib
import json

server_port: int = 0
config_daten_individuell_gesamt: dict = {}
config_daten_allgemein_gesamt: dict = {}
log_dateien_url: str = ""
log_level_url: str = ""
log_daten_microservice_name: dict = {}


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
    _verwendete_microservices: list = config_daten_individuell_gesamt["verwendete_microservices"]
    _microservice_daten: dict = {}
    for _microservice in _verwendete_microservices:
        _microservice_daten[_microservice] = config_daten_allgemein_gesamt["microservices"][_microservice]
    global log_dateien_url
    log_dateien_url = "http://" \
                      + "localhost:" \
                      + str(_microservice_daten["log_dateien"]["server_port"]) \
                      + _microservice_daten["log_dateien"]["route"]
    global log_level_url
    log_level_url = "http://" \
                      + "localhost:" \
                      + str(_microservice_daten["log_level"]["server_port"]) \
                      + _microservice_daten["log_level"]["route"]

    return None


class Logging:

    def __init__(self):
        self._log_daten = ""
        self._log_file = 'logging.txt'
        self._current_working_directory = pathlib.Path.cwd()
        self._current_working_file: str = str(self._current_working_directory) + "\\" + self._log_file
        self._zusatzdaten_ein: dict = {}

    def hole_zusatzdaten(self, name_microservice: str): # Log-Dateien, Log-Level
        self._log_dateien_anfrage = urllib.request.Request(url = log_dateien_url, method = "GET")
        self._log_dateien_daten = urllib.request.urlopen(self._log_dateien_anfrage)
        self._log_dateien_daten = json.load(self._log_dateien_daten)
        _name_microservice_aus = json.dumps(name_microservice).encode("utf-8")
        self._log_level_anfrage = urllib.request.Request(url = log_level_url, method = "GET")
        self._log_level_anfrage.add_header('Content-Type', "application/json; charset=utf-8")
        self._log_level_anfrage.add_header('Content-Length', len(_name_microservice_aus))
        self._log_level_daten = urllib.request.urlopen(self._log_level_anfrage, _name_microservice_aus)
        self._log_level_daten = json.load(self._log_level_daten)
        self._zusatzdaten_ein["log_dateien"] = self._log_dateien_daten
        self._zusatzdaten_ein["log_level"] = self._log_level_daten

        return self._zusatzdaten_ein

    def bestimme_reihenfolge_log_daten(self, zusatzdaten_ein):
        _zusatzdaten_aus: str = {}
        _inhalte_zusatzdaten: list = []
        _inhalte_daten_microservice: list = []
        for _daten_microservice in zusatzdaten_ein["daten_microservice"]:
            for _schluessel in _daten_microservice:
                _inhalte_daten_microservice.append(_schluessel + ": " + str(_daten_microservice[_schluessel]))
        _inhalte_zusatzdaten.append(zusatzdaten_ein["zeitstempel"])
        _inhalte_zusatzdaten.append(zusatzdaten_ein["ID"])
        _inhalte_zusatzdaten.append(zusatzdaten_ein["name_microservice"])
        _inhalte_zusatzdaten.extend(_inhalte_daten_microservice)
        _inhalte_zusatzdaten.append(str(zusatzdaten_ein["status_code"]))
        _inhalte_zusatzdaten.append("\n")
        _zusatzdaten_aus = " | ".join(_inhalte_zusatzdaten)

        return _zusatzdaten_aus

    def get(self):

        return "OK GET"

    def post(self, _logging_data, zusatzdaten_ein: dict):
        _log_datei_permanent: str = zusatzdaten_ein["log_dateien"]["log_datei_permanent"]
        _log_datei_periodisch: str = zusatzdaten_ein["log_dateien"]["log_datei_periodisch"]
        with open(_log_datei_permanent, mode = "a") as _log_datei_permanent_obj_ein:
            _log_datei_permanent_obj_ein.write(str(_logging_data))
            print("schreibe in permanente Datei")
        if zusatzdaten_ein["log_level"] == True:
            with open(_log_datei_periodisch, mode="a") as _log_datei_periodisch_obj_ein:
                _log_datei_periodisch_obj_ein.write(str(_logging_data))
                print("schreibe in periodische Datei")

        return "Log-Daten erfasst"

    def put(self):

        return "OK PUT"

    def delete(self):

        return "OK DELETE"


app = Flask(__name__)

@app.route("/logging", methods = ["GET", "POST", "PUT", "DELETE"])
def ms_logging():
    global log_daten_microservice_name
    _logging = Logging()
    _logging._log_daten = request.get_json()
    log_daten_microservice_name = _logging._log_daten["name_microservice"]
    _logging._log_daten_neu = _logging.bestimme_reihenfolge_log_daten(_logging._log_daten)
    _logging._zusatzdaten_ein = _logging.hole_zusatzdaten(log_daten_microservice_name)
    if request.method == "GET":
        _logging = _logging.get()
    elif request.method == "POST":
        _logging = _logging.post(_logging._log_daten_neu, _logging._zusatzdaten_ein)
    elif request.method == "PUT":
        _logging = _logging.put()
    elif request.method == "DELETE":
        _logging = _logging.delete()

    return _logging



if __name__ == "__main__":
    _logging_config_daten_ein = lade_configdaten()
    verteile_configdaten(_logging_config_daten_ein)
    app.run(port = server_port, debug = True)