"""
Das ist die Bibliothek der Klasse Persistenz
"""

import json
import random
from datetime import datetime
import sys
import collections
import API_UF
import CRUD_Rueckmeldung_UF


class Baum:

    def __init__(self, wurzel: str):
        self.wurzel_ein: str = wurzel
        self.kinder: list = []


class Knoten:
    def __init__(self):
        self.schluessel_ressource: str = ""
        self.speicherinhalt = Speicherinhalt()
        self.eltern: str = ""
        self.kinder: list = []

    def __str__(self):
        self.inhalt_knoten: dict = {}
        self.inhalt_knoten["Ressource"] = self.schluessel_ressource
        self.inhalt_knoten["Kinder"] = self.kinder
        self.inhalt_knoten["Eltern"] = self.eltern
        self.inhalt_knoten["Speicherinhalt"] = self.speicherinhalt

        return self.inhalt_knoten


class Speicherinhalt:

    def __init__(self):
        self.speicherobjekt: dict = {}


class Persistenz:

    def __init__(self, wurzel: str, datenspeicher = False, speicherart: str = "Hauptspeicher"):
        self.__persistenz_datenspeicher = datenspeicher  # steuert, ob die Daten im Datenspeicher abgelegt werden
        self.datenspeicher: dict = {wurzel: {}} # legt einen neuen leeren Datenspeicher für den Microservice an
        self.speicherart: str = speicherart

    def zerlege_pfad(self, pfad: str) -> list:
        __pfad: str = pfad
        __hierarchien: list = [""]
        if __pfad[-1] == "/":
            __pfad = __pfad.rstrip("/")
            # Um ein leeres Listenelement zu vermeiden, wird ein mögliches "/" auf der letzten Position gelöscht
        __hierarchien.extend(__pfad.split("/"))
        for __elemente in __hierarchien:
            if __elemente == "":
                __hierarchien.remove("")

        return __hierarchien

    def erzeuge_schluessel_neueintrag(self, nummer_ein: int) -> str:
        """

        :param nummer_ein:
        :return:
        """
        __nummer_ein = nummer_ein
        __schluessel: str = ""
        __schluessel = str(__nummer_ein) + "_" + str((random.randint(1, 1000) * random.randint(1, 1000)))

        return __schluessel

    def ermittele_letzten_eintrag_hierarchie(self, hierarchie_ein: list) -> int:
        __hierarchie_ein = hierarchie_ein
        __ressourcen: list = [0]
        for __eintrag in __hierarchie_ein:
            if not __eintrag.startswith("h_"):  # schließt Hierachien bei der Betrachtung aus
                __ressourcen.append(int(__eintrag))  # erfasse vorhandene Ressourcen in Hierachie

        return max(__ressourcen)

    def zeige_datenspeicher_json(self, hierarchie_ein: dict):
        """
        Da der Inhalt eines Dictionaries in einer Zeile angezeigt wird, sind die einzelnen Hierarchien schwer zu
        erkennen. Mit der Methode erfolgt die Anzeige in Form eines JSON-Formats. Zur besseren Übersichtlichkeit
        werden die Schluessel-Wert-Paare alphabetisch sortiert.
        :param hierarchie_ein:
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
        __neues_speicherelement = Speicherinhalt()
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
            __rueckgaben_daten_aus["daten"] = __neues_speicherelement.speicherobjekt
            print(type(__neues_speicherelement.speicherobjekt))
            __rueckgaben_daten_aus["erzeuge_ressource_erfolgreich"] = True
            __rueckgaben_daten_aus["fehlercode"] = 201

        return json.dumps(__rueckgaben_daten_aus)

    def lese_speicherinhalt(self, ebenen: list) -> json:  # Ergänzung Parameter: Benutzer-ID, Passwort, Suchschlüssel)
        """

        Grundlage: CRUD - Read
        :return:
        """
        __ebenen = ebenen
        __rueckgaben_daten_aus: dict = {"speicherinhalt": None,
                                        "rueckmeldung": "",
                                        "lese_ressource_erfolgreich": False,
                                        "fehlercode": 0}
        __ressource_vorhanden: bool = True
        __aktuelle_ebene = self.datenspeicher
        for __schluesselwort in __ebenen:
            try:
                __aktuelle_ebene = __aktuelle_ebene[__schluesselwort]
            except KeyError:
                print("Ebene", __aktuelle_ebene, "nicht vorhanden")
                __ressource_vorhanden = False
                __rueckgaben_daten_aus["rueckmeldung"] = f"Ressource {'/'.join(ebenen)} nicht vorhanden"
                __rueckgaben_daten_aus["speicherinhalt"] = {}
                break
        if __ressource_vorhanden:
            __rueckgaben_daten_aus["speicherinhalt"] = __aktuelle_ebene
            __rueckgaben_daten_aus["rueckmeldung"] = f"Ressource {'/'.join(ebenen)} erfolgreich abgerufen"
            __rueckgaben_daten_aus["lese_ressource_erfolgreich"] = True

        return json.dumps(__rueckgaben_daten_aus)

    def aendere_speicherinhalt(self, ebenen: list, inhalt_ein: dict):
        """

        Grundlage: CRUD - Update
        :return:
        """
        __ebenen = ebenen
        __inhalt_ein = inhalt_ein
        __rueckgaben_daten_aus: dict = {"speicherinhalt": None,
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
        __rueckgabe_daten_aus_nutzer: dict = {"speicherinhalt": None,
                                              "rueckmeldung": ""
                                              }
        __rueckgaben_daten_aus_entwickler: dict = {"loesche_ressource_erfolgreich": False,
                                                   "fehlercode": 0
                                                   }
        __rueckgaben_daten_aus: dict = {"speicherinhalt": None,
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
