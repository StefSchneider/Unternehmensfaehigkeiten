"""
Der Microservice erstellt einen Zeitstempel auf Basis der aktuellen Zeit und einen Zeitstempel auf Basis der UTC-Zeit.
Die Daten werden im JSON-Fomat zurückgegeben.
"""

import API_UF
from flask import Flask, request, jsonify
import datetime

server_port: int = 31005

eigener_pfad = "http://localhost:31005/zeitstempel"
eigener_pfad_kurz = "/zeitstempel"


class Zeitstempel:

    def __init__(self):
        self.__zeitstempel_lokal: str = ""
        self.__zeitstempel_UTC: str = ""
        self.__zeitstempel_UTC_original: str = ""
        self.__zeitstempel_genau: str = ""
        self.__zeitstempel_daten: dict = {}

    def hole(self):
        self.__zeitstempel_UTC_original = datetime.datetime.now(datetime.timezone.utc)
        self.__zeitstempel_lokal = self.__zeitstempel_UTC_original.replace(tzinfo = datetime.timezone.utc)
        self.__zeitstempel_lokal = self.__zeitstempel_lokal.astimezone(tz = None)
        self.__zeitstempel_lokal = self.__zeitstempel_lokal.strftime("%Y-%m-%d %H:%M:%S %z")
        self.__zeitstempel_UTC = self.__zeitstempel_UTC_original.strftime("%Y-%m-%d %H:%M:%S %z")
        self.__zeitstempel_genau = self.__zeitstempel_UTC_original.strftime("%Y-%m-%d %H:%M:%S %f")
        self.__zeitstempel_daten["zeitstempel_lokal"] = self.__zeitstempel_lokal
        self.__zeitstempel_daten["zeitstempel_UTC"] = self.__zeitstempel_UTC
        self.__zeitstempel_daten["zeitstempel_UTC_original"] = self.__zeitstempel_UTC_original
        self.__zeitstempel_daten["zeitstempel_genau"] = self.__zeitstempel_genau

        return self.__zeitstempel_daten

    def schreibe(self):
        self.__zeitstempel_lokal = "0000:00:00 00:00:00"
        self.__zeitstempel_UTC = "0000:00:00 00:00:00"
        self.__zeitstempel_daten["zeitstempel_lokal"] = self.__zeitstempel_lokal
        self.__zeitstempel_daten["zeitstempel_UTC"] = self.__zeitstempel_UTC

        return self.__zeitstempel_daten

    def ueberschreibe(self):
        self.__zeitstempel_lokal = "0000:00:00 00:00:00"
        self.__zeitstempel_UTC = "0000:00:00 00:00:00"
        self.__zeitstempel_daten["zeitstempel_lokal"] = self.__zeitstempel_lokal
        self.__zeitstempel_daten["zeitstempel_UTC"] = self.__zeitstempel_UTC

        return self.__zeitstempel_daten

    def aendere(self):
        self.__zeitstempel_lokal = "0000:00:00 00:00:00"
        self.__zeitstempel_UTC = "0000:00:00 00:00:00"
        self.__zeitstempel_daten["zeitstempel_lokal"] = self.__zeitstempel_lokal
        self.__zeitstempel_daten["zeitstempel_UTC"] = self.__zeitstempel_UTC

        return self.__zeitstempel_daten

    def loesche(self):
        self.__zeitstempel_lokal = "OK Lokal"
        self.__zeitstempel_UTC = "OK UTC"
        self.__zeitstempel_daten["zeitstempel_lokal"] = self.__zeitstempel_lokal
        self.__zeitstempel_daten["zeitstempel_UTC"] = self.__zeitstempel_UTC

        return self.__zeitstempel_daten


app = Flask(__name__)


@app.route("/zeitstempel", methods = ["GET", "POST", "PUT", "PATCH", "DELETE"])
def zeitstempel() -> str:
    zeitstempel_API = API_UF.API(get_request_zulassen = True, post_request_zulassen = True,
                                 put_request_zulassen = True, patch_request_zulassen = True,
                                 delete_request_zulassen = True)
    __zeitstempel = Zeitstempel()
    __zeitstempel_obj_aus: dict = {}
    if request.method == "GET":
        if zeitstempel_API.get_request_erlaubt:
            __zeitstempel = __zeitstempel.hole()
            __zeitstempel = zeitstempel_API.get(__zeitstempel)
        else:
            return "GET-Request nicht erlaubt"
    elif request.method == "POST":
        if zeitstempel_API.post_request_erlaubt:
            __zeitstempel = __zeitstempel.schreibe()
        else:
            return "POST-Request nicht erlaubt"
    elif request.method == "PUT":
        if zeitstempel_API.put_request_erlaubt:
            __zeitstempel = __zeitstempel.ueberschreibe()
        else:
            return "PUT-Request nicht erlaubt"
    elif request.method == "PATCH":
        if zeitstempel_API.patch_request_erlaubt:
            __zeitstempel = __zeitstempel.aendere()
        else:
            return "PATCH-Request nicht erlaubt"
    elif request.method == "DELETE":
        if zeitstempel_API.delete_request_erlaubt:
            __zeitstempel = __zeitstempel.loesche()
        else:
            return "DELETE-Request nicht erlaubt"
    __zeitstempel_obj_aus["zeitstempel_lokal"] = __zeitstempel["zeitstempel_lokal"]
    __zeitstempel_obj_aus["zeitstempel_UTC"] = __zeitstempel["zeitstempel_UTC"]
    __zeitstempel_obj_aus["zeitstempel_UTC_original"] = __zeitstempel["zeitstempel_UTC_original"]
    __zeitstempel_obj_aus["zeitstempel_genau"] = __zeitstempel["zeitstempel_genau"]

    return jsonify(__zeitstempel_obj_aus)


if __name__ == "__main__":
    app.run(port = server_port, debug = True)
