"""
Der Microservice erhaelt per PUT vom Microservice hellos eine Textzeile und den Auftrag.
Zudem erhaelt er vom Microservice hellos_updates per GET eine Anfrage nach der Textzeile und liefert diese zurück
Er druckt die Textzeile aus, wenn der Auftrag auf "drucke_daten" steht
"""

import API_UF
import Persistenz_UF as PRS
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

id = 0
prints_PRS = PRS.Persistenz("prints", datenspeicher = True)

app = Flask(__name__)
@app.route("/<path:pfad>", methods = ["GET", "POST", "PUT", "PATCH", "DELETE"])
def drucke(pfad):
    print("Pfad: ", pfad)
    prints_API = API_UF.API(get_request_zulassen = True, post_request_zulassen =  True, put_request_zulassen = True,
                            patch_request_zulassen = True, delete_request_zulassen = True)
    prints_API.url_partner = "http://localhost:31001/hellos"
    rueckmeldung: dict = {}
    __rueckmeldung_request_verarbeitung = API_UF.REST_Rueckmeldung(entwickler_informationen_anzeigen = True)
    drucke_daten: bool = False
    text_zum_drucken: str = ""
    __hierarchien: list = prints_PRS.zerlege_pfad(pfad)
    if request.method == "GET":
#        __rueckmeldung_get_verarbeitung = json.loads(__rueckmeldung_request_verarbeitung.rueckmeldung_objekte_fuellen_get())
        if prints_API.get_request_erlaubt:
            __inhalt_speicher = json.loads(prints_PRS.get_request_in_crud(__hierarchien))
            __inhalt_speicher_aus = prints_API.get(__inhalt_speicher)
            return (__inhalt_speicher_aus)
        else:
            return "GET-Request nicht erlaubt"
    elif request.method == "POST":
        if prints_API.post_request_erlaubt:
            uebergabedaten_ein = request.get_json()
            rueckmeldung = prints_API.post(uebergabedaten_ein)
            __schluessel_neue_ressource = prints_PRS.erzeuge_schluessel_neueintrag(int(rueckmeldung["id"]))
            neuer_eintrag_in_datenspeicher: dict = {__schluessel_neue_ressource: rueckmeldung.copy()}
            text_zum_drucken = rueckmeldung["daten"]
            neuer_speicher = prints_PRS.post_request_in_crud(__hierarchien, neuer_eintrag_in_datenspeicher)
            print("Neuer Eintrag", neuer_eintrag_in_datenspeicher)
            if rueckmeldung["auftrag"] == "drucke_daten":
                drucke_daten = True
        else:
            return "POST-Request nicht erlaubt"
    elif request.method == "PUT":
        if prints_API.put_request_erlaubt:
            uebergabedaten_ein = request.get_json()
            rueckmeldung = prints_API.put(uebergabedaten_ein)
            __schluessel_ressource = __hierarchien[-1]
            __eintrag_in_datenspeicher: dict = {__schluessel_ressource: rueckmeldung.copy()}
            neuer_speicher = prints_PRS.put_request_in_crud(__hierarchien, __eintrag_in_datenspeicher)
            print("Neuer Eintrag", __eintrag_in_datenspeicher)
            text_zum_drucken = rueckmeldung["daten"]
            if rueckmeldung["auftrag"] == "drucke_daten":
                drucke_daten = True
            else:
                drucke_daten = False
        else:
            return "PUT-Request nicht erlaubt."
    elif request.method == "PATCH":
        if prints_API.patch_request_erlaubt:
            uebergabedaten_ein = request.get_json()
            rueckmeldung = prints_API.patch(uebergabedaten_ein)
            __neuer_speicher  = prints_PRS.patch_request_in_crud(__hierarchien, rueckmeldung)
            try:
                text_zum_drucken = rueckmeldung["daten"]
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
            uebergabedaten_ein = request.get_json()
            prints_PRS.delete_request_in_crud(__hierarchien)
            rueckmeldung = prints_API.delete(uebergabedaten_ein)
        else:
            return ("DELETE-Request nicht erlaubt")
    else:
        print("API-Fehler!!!")
    if drucke_daten:
        print("Jetzt wird ein Text gedruckt: ", text_zum_drucken)
    prints_PRS.zeige_datenspeicher_json(prints_PRS.datenspeicher)

    return jsonify(prints_PRS.datenspeicher)


if __name__ == "__main__":
    app.run(port = server_port, debug = True)
