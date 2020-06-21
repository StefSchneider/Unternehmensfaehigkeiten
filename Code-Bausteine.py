"""
Das Skript enthält Code-Bausteine, die in vielen der Microservices verwendet werden können.
"""

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


def get(self):

    return "OK GET"

def post(self):

    return "OK POST"

def put(self):

    return "OK PUT"

def delete(self):

    return "OK DELETE"


