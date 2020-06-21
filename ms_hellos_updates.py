"""
Dieser Microservice ändert per PATCH die Daten für die Textzeile und den Auftrag beim Microservice hellos.
Zudem fragt er per GET die aktuelle Textzeile an.
"""

import API_UF
import sys

eigener_server_port: int = 31003

if __name__ == "__main__":
    while True:
        hellos_updates_API = API_UF.API()
        nummer_ressource: int = input("Auf welche Ressource möchten Sie zugreifen (Nr.)? ")
        hellos_updates_API.url_partner = "http://localhost:31002/prints/" + str(nummer_ressource)
        aktuelle_daten_prints = hellos_updates_API.hole({})
        print(aktuelle_daten_prints)
        uebergabedaten_aus = {}
        auswahl = input("Was möchten Sie ändern? 1 = Daten, 2 = Auftrag: ")
        if auswahl == "1":
            neuer_uebergabetext: str = input("Welcher neue Text soll gedruckt werden: ")
            uebergabedaten_aus["daten"] = neuer_uebergabetext
        elif auswahl == "2":
            auswahl_auftrag: str = input("Auftrag neu? 1 = drucke_daten, 2 = drucke_nicht: ")
            if auswahl_auftrag == "1":
                uebergabedaten_aus["auftrag"] = "drucke_daten"
            else:
                uebergabedaten_aus["auftrag"] = "drucke_nicht"
        else:
            print("Auswahlfehler!!!")
        uebergabedaten_aus["auftraggeber"] = sys.argv[0]
        print(uebergabedaten_aus)
        hellos_updates_API.url_partner = "http://localhost:31002/prints/" + str(nummer_ressource)
        hellos_updates_API.aendere(uebergabedaten_aus)

