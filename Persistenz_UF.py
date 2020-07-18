"""
Das ist die Bibliothek der Klasse Persistenz
"""

import json
from flask import jsonify
import random


ENTWICKLER_INFORMATIONEN: bool = True

class REST_Rueckmeldung:

    def __init__(self, entwickler_informationen_anzeigen: bool = ENTWICKLER_INFORMATIONEN):
        self.__entwickler_informationen_anzeigen = entwickler_informationen_anzeigen
        self.__rueckmeldung:dict = {}
        self.__rueckmeldung_daten: dict = {"daten": None
                                           }
        self.__rueckmeldung_nutzer: dict = {"anzahl_speicherobjekte": None,
                                            "status": None,
                                            "suchschluessel": None,
                                            "anzahl_rueckgabeobjekte": None,
                                            "startobjekt": 0,
                                            "berechtigung": None,
                                            "daten_veraendert": None
                                            }
        self.__rueckmeldung_entwickler: dict = {"laenge_bytes": None,
                                                "verarbeitungszeit": None,
                                                "datenstruktur": None,
                                                "strukturtiefe": None,
                                                "speicherart": None
                                                }
        self.__rueckmeldung_programm: dict = {"datentyp_rueckgabeobjekt": None
                                              }



class Persistenz:

    def __init__(self, wurzel: str, datenspeicher = False):
        self.__persistenz_datenspeicher = datenspeicher # steuert, ob die Daten im Datenspeicher abgelegt werden
        self.datenspeicher: dict = {wurzel: {}}

    def zerlege_pfad(self, pfad: str) -> list:
        __pfad = pfad
        __hierarchien: list = [""]
        if __pfad[-1] == "/":
            __pfad = __pfad.rstrip("/")
            # Um ein leeres Listenelement zu vermeiden, wird ein mögliches "/" auf der letzten Position gelöscht
        __hierarchien.extend(__pfad.split("/"))
        for __elemente in __hierarchien:
            if __elemente == "":
                __hierarchien.remove("")
        print("Liste der Hierachien:", __hierarchien)

        return __hierarchien

    def erzeuge_schluessel_neueintrag(self, nummer_ein: int) -> str:
        """

        :param nummer_ein:
        :return:
        """
        schluessel: str = ""
        schluessel = str(nummer_ein) + "_" + str((random.randint(1,1000) * random.randint(1,1000)))

        return schluessel

    def ermittele_letzten_eintrag_hierarchie(self, hierarchie_ein: list) -> int:
        __ressourcen: list = [0]
        for __eintrag in hierarchie_ein:
            if not __eintrag.startswith("h_"): # schließt Hierachien bei der Betrachtung aus
                __ressourcen.append(int(__eintrag)) # erfasse vorhandene Ressourcen in Hierachie

        return(max(__ressourcen))

    def zeige_datenspeicher_json(self, hierarchie_ein: dict):
        """
        Da der Inhalt eines Dictionaries in einer Zeile angezeigt wird, sind die einzelnen Hierarchien schwer zu
        erkennen. Mit der Methode erfolgt die Anzeige in Form eines JSON-Formats. Zur besseren Übersichtlichkeit
        werden die Schluessel-Wert-Paare alphabetisch sortiert.
        :param hierachie_ein:
        :return: None
        """
        __datenspeicher_json = json.dumps(hierarchie_ein, sort_keys = True, indent = 4)
        print(__datenspeicher_json)

    def ersetze_letzen_schluessel(self, ebenen: list) -> list:
        """
        Hierarchien sind in dem Dictionary mit dem Prefix "h_" gekennzeichnet. Der tatsächliche Speicher innerhalb der
        Hierarchie enthält kein solches Prexif. Um auf den Wert des angeforderten Speichers zugreifen zu können, muss
        das Prexif des letzten Schlüssels abgeschnitten werden.
        :param ebenen: Liste der Hierarchien
        :return: Liste der Hierarchien mit dem geänderten letzten Schlüsselwort
        """
        __ebenen = ebenen
        __letztes_schluesselwort = __ebenen[-1]
        __letztes_schluesselwort = __letztes_schluesselwort.rsplit("/", 1)[1]
        __ebenen[-1] = __letztes_schluesselwort

        return __ebenen


    def erzeuge_speicherinhalt(self, ebenen: list, inhalt: dict):
        """
        Mit der Methode wird ein leeres Speicherelement unter der richtigen Ressource angelegt, das später über die
        Methode aendere_speicherinhalt gefüllt wird.
        Grundlage: CRUD - Create
        :return: neu angelegtes Speicherelement als leeres Dictionary
        """
        __ebenen = ebenen
        __inhalt = inhalt
#        __neuer_schluessel = neuer_schluessel
        __neues_speicherelement: dict = {}
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "erzeuge_ressource_erfolgreich": False,
                                        "fehlercode": 0}
        __ressource_vorhanden: bool = True
        __aktuelle_ebene = self.datenspeicher

        for __position, __schluessel in enumerate(ebenen):
            if __schluessel in __aktuelle_ebene.keys():
                __aktuelle_ebene = __aktuelle_ebene[__schluessel]
            else:
                __rueckgaben_daten_aus["rueckmeldung"] = "Ressource kann nicht angelegt werden:" \
                                                         + " ... " \
                                                         + "/".join(ebenen[__position - 1:]) \
                                                         + " fehlt."
                __ressource_vorhanden = False
                break
        if __ressource_vorhanden:
            __aktuelle_ebene.update(__inhalt)
            __rueckgaben_daten_aus["daten"] = __neues_speicherelement
            __rueckgaben_daten_aus["erzeuge_ressource_erfolgreich"] = True
            __rueckgaben_daten_aus["fehlercode"] = 201

        print("Rückgabe erzeuge_speicherinhalt:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def lese_speicherinhalt(self, ebenen: list) -> dict:
        """

        Grundlage: CRUD - Read
        :return:
        """
        __ebenen = ebenen
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "lese_ressource_erfolgreich": False,
                                        "fehlercode": 0}
        __ressource_vorhanden: bool = True
        __aktuelle_ebene = self.datenspeicher
        for __schluesselwort in __ebenen:
            try:
                __aktuelle_ebene = __aktuelle_ebene[__schluesselwort]
            except KeyError:
                __ressource_vorhanden = False
                __rueckgaben_daten_aus["rueckmeldung"] = f"Ressource {'/'.join(ebenen)} nicht vorhanden"
                break
        if __ressource_vorhanden:
            __rueckgaben_daten_aus["daten"] = __aktuelle_ebene
            __rueckgaben_daten_aus["rueckmeldung"] = f"Ressource {'/'.join(ebenen)} erfolgreich abgerufen"
            __rueckgaben_daten_aus["lese_ressource_erfolgreich"] = True

        print("Rückgabe lese_speicherinhalt:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def aendere_speicherinhalt(self, ebenen: list, inhalt_ein: dict):
        """

        Grundlage: CRUD - Update
        :return:
        """
        __ebenen = ebenen
        __inhalt_ein = inhalt_ein
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "aendere_ressource_erfolgreich": False,
                                        "fehlercode": 0}
        __aktuelle_ebene = self.datenspeicher
        for __position, __schluessel in enumerate(__ebenen):
            if __position == len(__ebenen) - 1:
                __aktuelle_ebene = __inhalt_ein
            else:
                __aktuelle_ebene = __aktuelle_ebene[__schluessel]

        print("Rückgabe aendere_speicherinhalt:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def loesche_speicherinhalt(self, ebenen: list):
        """
        
        Grundlage: CRUD - Delete
        :return:
        """
        __ebenen = ebenen
        __rueckgabe_daten_aus_nutzer: dict = {"daten": None,
                                              "rueckmeldung": ""
                                              }
        __rueckgaben_daten_aus_entwickler: dict = {"loesche_ressource_erfolgreich": False,
                                                   "fehlercode": 0
                                                   }
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "loesche_ressource_erfolgreich": False,
                                        "fehlercode": 0}
        __aktuelle_ebene = self.datenspeicher
        for __position, __schluesselwort in enumerate(__ebenen):
            try:
                if __position == len(__ebenen) - 1:
                    del(__aktuelle_ebene[__schluesselwort])
                    __rueckgaben_daten_aus["rueckmeldung"] = "Ressource gelöscht"
                    __rueckgaben_daten_aus["loesche_ressource_erfolgreich"] = True
                    __rueckgaben_daten_aus["fehlercode"] = 200
                else:
                    __aktuelle_ebene = __aktuelle_ebene[__schluesselwort]
            except KeyError:
                __rueckgaben_daten_aus["rueckmeldung"] = "Ressource nicht vorhanden"
                __rueckgaben_daten_aus["fehlercode"] = 401
                break

        print("Rückgabe loesche_speicherinhalt:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def get_request_in_crud(self, ebenen_ein: list) -> json:
        """
        1. Read
        :return:
        """
        __ebenen: list = ebenen_ein
        __rest_rueckmeldung_get = REST_Rueckmeldung()
        __speicherinhalt: dict = {}
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "fehlercode": 0}

        __rest_rueckmeldung_get.__rueckmeldung_daten["daten"] = json.loads(self.lese_speicherinhalt(__ebenen))
        __rueckgaben_daten_aus["daten"] = __rest_rueckmeldung_get.__rueckmeldung_daten["daten"]

        print("Rückgabe get_request_in_crud:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def post_request_in_crud(self, ebenen: list, inhalt_ein: dict) -> json:
        """
        1. Create
        2. Update
        :return:
        """
        __ebenen = ebenen
        __inhalt_ein = inhalt_ein
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "fehlercode": 0}
        __aktuelle_ebene = self.datenspeicher
        __neues_speicherelement = json.loads(self.erzeuge_speicherinhalt(__ebenen, __inhalt_ein))
        if __neues_speicherelement["erzeuge_ressource_erfolgreich"]:

            __neues_speicherelement = json.loads(self.aendere_speicherinhalt(__ebenen, __inhalt_ein))
        else:
            print(__neues_speicherelement["rueckmeldung"])

        print("Rückgabe post_request_in_crud:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def put_request_in_crud(self, ebenen: list, inhalt_ein: dict) -> json:
        """
        1. Delete
        2. Create
        3. Update
        2. + 3. = POST
        :return:
        """
        __ebenen = ebenen
        __inhalt_ein = inhalt_ein
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "fehlercode": 0}

        speicherelement = json.loads(self.loesche_speicherinhalt(__ebenen))
        __ebenen = ebenen[:len(ebenen) - 1]
        speicherelement = json.loads(self.post_request_in_crud(__ebenen, __inhalt_ein))

        print("Rückgabe put_request_in_crud:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def patch_request_in_crud(self, ebenen: list, inhalt_ein: dict) -> json:
        """
        1. Read
        2. Werte überschreiben
        3. Delete
        4. Create
        5. Update
        3. + 4. + 5. = PUT
        :return:
        """
        __ebenen = ebenen
        __inhalt_ein = inhalt_ein
        __aktuelles_speicherelement: dict = {}
        __schluessel_ressource = __ebenen[-1]
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "fehlercode": 0}

        __aktuelles_speicherelement = json.loads(self.lese_speicherinhalt(__ebenen))
        __aktuelles_speicherelement = __aktuelles_speicherelement["daten"]
        for __schluessel in __inhalt_ein:
            try:
                __aktuelles_speicherelement[__schluessel] = __inhalt_ein[__schluessel]
            except KeyError:
                print(f"Schlüssel {__schluessel} nicht vorhanden")
        __speicherlement = self.put_request_in_crud(__ebenen, {__schluessel_ressource: __aktuelles_speicherelement})

        print("Rückgabe patch_request_in_crud:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)
    
    def delete_request_in_crud(self, ebenen) -> json:
        """
        1. Delete
        :return:
        """
        __ebenen = ebenen
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "fehlercode": 0}
        __speicherelement_loeschen = self.loesche_speicherinhalt(__ebenen)
        __speicherelement_loeschen = json.loads(__speicherelement_loeschen)
        if __speicherelement_loeschen["rueckmeldung"] != "":
            print(__speicherelement_loeschen["rueckmeldung"])
        __rueckgaben_daten_aus["rueckmeldung"] = f"Element {__ebenen[-1]} aus Speicher gelöscht"

        print("Rückgabe delete_request_in_crud:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)