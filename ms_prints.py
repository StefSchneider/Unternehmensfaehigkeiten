"""
Der Microservice erhaelt per PUT vom Microservice hellos eine Textzeile und den Auftrag.
Zudem erhaelt er vom Microservice hellos_updates per GET eine Anfrage nach der Textzeile und liefert diese zurück
Er druckt die Textzeile aus, wenn der Auftrag auf "drucke_daten" steht
"""

import API_UF
import Persistenz_UF as PRS
import Service_Logik_UF
from flask import Flask, request, jsonify
import json


datensatz: dict = {"auftrag": None,
                   "daten": None,
                   "auftraggeber": None,
                   "server_port_auftraggeber": None
                   }

eigener_pfad = "http://localhost:31002/prints"
eigener_pfad_kurz = "/prints"

server_port: int = 31002

prints_PRS = PRS.Persistenz("prints", datenspeicher = True, speicherart = "Hauptspeicher")
prints_CRUD_Rueckmeldung = Service_Logik_UF.CRUD_Rueckmeldung(prints_PRS)

app = Flask(__name__)


@app.route("/<path:pfad>", methods = ["GET", "POST", "PUT", "PATCH", "DELETE"])
def drucke(pfad):
    prints_API = API_UF.API(get_request_zulassen = True, post_request_zulassen = True, put_request_zulassen = True,
                            patch_request_zulassen = True, delete_request_zulassen = True)
    prints_API.url_partner = "http://localhost:31001/hellos"

    rueckmeldung: dict = {}
    __rueckmeldung_request_verarbeitung = API_UF.REST_Rueckmeldung(entwickler_informationen_anzeigen = True)
    drucke_daten: bool = False
    text_zum_drucken: str = ""
    __hierarchien: list = prints_PRS.zerlege_pfad(pfad)
    if request.method == "GET":
        __rueckmeldung_get_verarbeitung = \
            json.loads(__rueckmeldung_request_verarbeitung.rueckmeldung_objekte_filtern_get())
        if prints_API.get_request_erlaubt:
            __rueckmeldung_get_request_verarbeitung = \
                json.loads(prints_CRUD_Rueckmeldung.get_request_in_crud(__hierarchien))
            __rueckmeldung_get_request_verarbeitung_aus = __rueckmeldung_get_request_verarbeitung
#            __rueckmeldung_get_request_verarbeitung_aus = prints_API.get(__rueckmeldung_get_request_verarbeitung)
            return __rueckmeldung_get_request_verarbeitung
        else:
            return "GET-Request nicht erlaubt"
    elif request.method == "POST":
        if prints_API.post_request_erlaubt:
            rueckmeldung = prints_API.post()  # hier werden die Daten in ein dict umgewandelt
            __schluessel_neue_ressource = prints_PRS.erzeuge_schluessel_neueintrag(int(rueckmeldung["id"]))
            neuer_eintrag_in_datenspeicher: dict = {__schluessel_neue_ressource: rueckmeldung.copy()}
            text_zum_drucken = rueckmeldung["text"]
            prints_CRUD_Rueckmeldung.post_request_in_crud(__hierarchien, neuer_eintrag_in_datenspeicher)
            if rueckmeldung["auftrag"] == "drucke_daten":
                drucke_daten = True
        else:
            return "POST-Request nicht erlaubt"
    elif request.method == "PUT":
        if prints_API.put_request_erlaubt:
            rueckmeldung = prints_API.put()
            __schluessel_ressource = __hierarchien[-1]
            __eintrag_in_datenspeicher: dict = {__schluessel_ressource: rueckmeldung.copy()}
            prints_CRUD_Rueckmeldung.put_request_in_crud(__hierarchien, __eintrag_in_datenspeicher)
            text_zum_drucken = rueckmeldung["text"]
            if rueckmeldung["auftrag"] == "drucke_daten":
                drucke_daten = True
            else:
                drucke_daten = False
        else:
            return "PUT-Request nicht erlaubt."
    elif request.method == "PATCH":
        if prints_API.patch_request_erlaubt:
            rueckmeldung = prints_API.patch()
            __neuer_speicher = prints_CRUD_Rueckmeldung.patch_request_in_crud(__hierarchien, rueckmeldung)
            try:
                text_zum_drucken = rueckmeldung["text"]
            except KeyError:
                pass
            try:
                if rueckmeldung["auftrag"] == "drucke_daten":
                    drucke_daten = True
                else:
                    drucke_daten = False
            except KeyError:
                pass
        else:
            return "PATCH-Request nicht erlaubt"
    elif request.method == "DELETE":
        if prints_API.delete_request_erlaubt:
            prints_CRUD_Rueckmeldung.delete_request_in_crud(__hierarchien)
            rueckmeldung = prints_API.delete()
        else:
            return "DELETE-Request nicht erlaubt"
    else:
        print("API-Fehler!!!")
    if drucke_daten:
        print("Jetzt wird ein Text gedruckt: ", text_zum_drucken)
    prints_PRS.datenspeicher.zeige_datenspeicher_json()
    prints_datenspeicher_dict = prints_PRS.datenspeicher.wandle_baum_in_dict()

    return jsonify(prints_datenspeicher_dict)


if __name__ == "__main__":
    app.run(port = server_port, debug = True)
