"""
Der Microservice uebertraegt per PUT eine Textzeile und einen Auftrag an den Microservice prints
"""


import API_UF
import Persistenz_UF as PRS
import sys


eigener_server_port: int = 31001

if __name__ == "__main__":
    while True:
        hellos_API = API_UF.API()
        hellos_PRS = PRS.Persistenz("prints", datenspeicher = True)
        hellos_API.url_partner = "http://localhost:31002/prints/"
        uebergabedaten_aus = {}
        nummer_ressource: str = input("Auf welche Ressource möchten Sie zugreifen? ")
        __id_nummer: str = input("Welche Identifikationsnummer soll angesprochen werden? ")
        auswahl = input("Was möchten Sie tun? 1 = holen, 2 = schreiben, 3 = überschreiben, 4 = löschen: ")
        if auswahl == "1":
            hellos_API.url_partner += str(nummer_ressource)
            uebergabedaten_ein = hellos_API.hole()
            hellos_PRS.zeige_datenspeicher_json(uebergabedaten_ein)
        elif auswahl == "2":
            uebergabetext: str = input("Welcher Text soll gedruckt werden?")
            if uebergabetext != "":
                uebergabedaten_aus["auftrag"] = "drucke_daten"
            else:
                uebergabedaten_aus["auftrag"] = "drucke_nicht"
            uebergabedaten_aus["id"] = __id_nummer
            uebergabedaten_aus["daten"] = uebergabetext
            uebergabedaten_aus["auftraggeber"] = sys.argv[0]
            uebergabedaten_aus["server_port_auftraggeber"] = eigener_server_port
            print(uebergabedaten_aus)
            print(hellos_API.url_partner)
            hellos_API.url_partner += str(nummer_ressource)
            hellos_API.schreibe(uebergabedaten_aus)
        elif auswahl == "3":
            uebergabetext: str = input("Welcher Text soll gedruckt werden?")
            if uebergabetext != "":
                uebergabedaten_aus["auftrag"] = "drucke_daten"
            else:
                uebergabedaten_aus["auftrag"] = "drucke_nicht"
            uebergabedaten_aus["daten"] = uebergabetext
            uebergabedaten_aus["id"] = __id_nummer
            uebergabedaten_aus["auftraggeber"] = sys.argv[0]
            uebergabedaten_aus["server_port_auftraggeber"] = eigener_server_port
            print(uebergabedaten_aus)
            hellos_API.url_partner += str(nummer_ressource)
            hellos_API.ueberschreibe(uebergabedaten_aus)
        elif auswahl == "4":
            hellos_API.url_partner += str(nummer_ressource)
            hellos_API.loesche()
            """
            loesche_alle_elemente: bool = False
            loesche_letztes_element: bool = False
            loesch_elemente = input("Welche Elemente sollen gelöscht werden? 1 = alle Elemente, 2 = letztes Element: ")
            if loesch_elemente == "1":
                uebergabedaten_aus["loesche_alle_elemente"] = True
            elif loesch_elemente == "2":
                uebergabedaten_aus["loesche_letztes_element"] = True
            else:
                print("Auswahlfehler")
            """
        else:
            print("Auswahlfehler!!!")
