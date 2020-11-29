"""
Das ist die Bibliothek der Klasse Persistenz
"""

import json
from flask import jsonify
import random
import API_UF


ENTWICKLER_INFORMATIONEN: bool = True


class CRUD_Rueckmeldung:

    def __init__(self, entwickler_informationen_anzeigen: bool = ENTWICKLER_INFORMATIONEN):
        self.__entwickler_informationen_anzeigen = entwickler_informationen_anzeigen
        self.__rueckmeldung: dict = {}
        self.rueckmeldung_daten: dict = {"daten": None
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

    def ermittle_speicherinhalt_daten_lese(self):
        """
        Die Methode liefert den Inhalt des Speicherobjekts (payload) bei einem GET-Request zurück.
        :return: Inhalt der Ressource
        """
        __daten_ressource: json = {}

        return __daten_ressource

    def ermittle_anzahl_speicherobjekte_nutzer_lese(self, daten_speicherobjekt: dict):
        """
        Die Methode ermittelt die Anzahl der Speicherobjekte zum angefragten Schlüssel. Dabei wird nur die erste
        Hierarchiestufe abgefragt, aber keine Unter-Dictionaries. Damit kann der Nutzer erkennen, wie viele Objekte
        in der Ressource, die er abfragt, abgespeichert sind. Er kann dann entscheiden, ob er seine Abfrage einschränkt,
        um weniger Daten zu erhalten. Die Berechnung erfolgt auf Basis der payload.
        :param: daten_speicherobjekt ist der Inhalt der payload
        :return: Anzahl der Speicherobjekte als Integer
        """
        __daten_speicherobjekt = daten_speicherobjekt
        __anzahl_daten_speicherobjekt: int = 0
        __anzahl_daten_speicherobjekt = len(__daten_speicherobjekt)

        return __anzahl_daten_speicherobjekt

    def ermittle_status_objekt_nutzer_lese(self):
        """
        Die Methode ermittelt, ob die angefragte Speicherobjekt überhaupt vorhanden ist.
        :return: Dictionary mit Einträgen True/False (bool) und "Ressource vorhanden"/"Ressource nicht vorhanden" (str)
        """
        __status_speicherobjekt: dict = {}
        __objekt_vorhanden: bool = False
        __rueckmeldung_objekt_vorhanden: str = "Ressource nicht vorhanden"
        # Hier die Prüfungsabfrage einfügen
        __status_speicherobjekt["objekt_vorhanden"] = __objekt_vorhanden
        __status_speicherobjekt["rueckmeldung"] = __rueckmeldung_objekt_vorhanden

        return __status_speicherobjekt

    def ermittle_status_suchschluessel_nutzer_lese(self):
        """
        Die Methode überprüft, ob der vom Nutzer angeforderte Suchschlüssel innerhalb der Payload überhaupt vorhanden
        ist. Basis ist der Inhalt der Payoad.
        :return: Dictionary mit Einträgen True/False (bool) und "Suchschlüssel vorhanden"/
        "Suchschlüssel nicht vorhanden" (str)
        """
        __status_suchschluessel: dict = {}
        __suchschluessel_vorhanden: bool = False
        __rueckmeldung_suchschluessel_vorhanden: str = "Suchschlüssel nicht vorhanden"
        # Hier die Prüfungsabfrage einfügen
        __status_suchschluessel["objekt_vorhanden"] = __suchschluessel_vorhanden
        __status_suchschluessel["rueckmeldung"] = __rueckmeldung_suchschluessel_vorhanden

        return __status_suchschluessel

    def ermittle_laenge_liste_speicherobjekte_nutzer_lese(self):
        """
        Die Methode ermittelt die Anzahl der tatsächlich zurückgegebenen Speicherobjekte, die unter dem angefragten
        Schlüssel hinterlegt sind. Derzeit ist diese gleich der Anzahl der Speicherobjekte, später kann eine Abweichung/
        Konkretisierung sinnvoll sein, wenn die ursprüngliche Nutzerabfrage die Zahl der zurückgegebenen Speicherobjekte
        einschränkt, aber die tatsächliche Zahl größer ist. In diesem Fall kann damit dem Nutzer signalisiert werden,
        dass noch mehr Speicherobjekte vorhanden sind und seine Abfrage unvollständig sein könnte. Die Berechnung
        erfolgt auf Basis der payload.
        :return: Anzahl der tatsächlichen Speicherobjekte als int
        """
        # derzeit = Anzahl der Speichelemente
        pass

    def ermittle_startobjekt_nutzer_lese(self):
        """
        Diese Methode ermittelt das vom Nutzer vorgegebene Startobjekt innerhalb der Liste der zurückgegebenen
        Speicherobjekte. Diese Methode ist später einsetzbar, wenn ein Nutzer die Daten der Ressource erst ab einem
        bestimmten Punkt sehen möchte, z.B. erst ab Objekt "xyz" aufwärts. Zunächst ist das Startobjekt immer 0. Die
        Berechnung erfolgt auf Basis der payload.
        :return: Position des Startobjekts in der Gesamtliste als int
        """
        pass

    def ermittle_zugriffsberechtigung_nutzer_lese(self, benutzer_id: str) -> bool:
        """
        Die Methode ermittelt, ob der Nutzer berechtigt ist, auf das Datenobjekt zuzugreifen. Dazu wird ist GET-Request
        an den Microservice ms_berechtigungen geschickt. Die Grundeinstellung wird auf 'False' gesetzt. Liegt eine
        Berechtigung vor, erfolgt wird die Variable __zugriff_erlaut auf 'True' gesetzt. Mithilfe von Berechtigungen
        können Zugriffe eingeschränkt werden.
        :param benutzer_id: Die ID, die individuell zu jedem Nutzer abespeichert ist
        :return: Berechtigung vorhanden/nicht vorhanden als bool
        """
        __benutzer_id = benutzer_id
        __zugriff_erlaubt: bool = False
        # Hier Abfrage der Benutzer-ID beim Microservice ms_berechtigungen einfügen

        return __zugriff_erlaubt

    def ermittle_status_daten_nutzer_lese(self):
        """
        Die Methode ermittelt, ob die Daten des angefragte Speicherobjekts noch aktuell sind oder während des Zugriffs
        verändert wurden. Dazu erfolgt eine Überprüfung, ob eine Änderung in der Queue vorliegt, die zeiltich vor oder
        gleich dem GET-Request auf die Ressource liegt. Falls ja, erfolgt eine entsprechende Rückmeldung an den Nutzer.
        Gibt "Daten sind nicht mehr aktuell" zurück, wenn diese während des Zugriffs verändert wurden.
        :return: ob Speicherobjekt verändert wurde als bool
        """
        __daten_speicherobjekt_veraendert: bool = False

        return __daten_speicherobjekt_veraendert

    def ermittle_speicherart_entwickler_lese(self):
        """
        Die Methode ermittelt die Speicherart, wo die Ressource abgelegt wurde, zum Beispiel Hauptspeicher, File oder
        Datenbank
        :return: Speicherart als str
        """
        __speicherart: str = ""

        return __speicherart

    def ermittle_laenge_daten_bytes_entwickler_lese(self):
        """
        Die Methode ermittelt die Größe der payload in Byte. Grundlage für die Berechnung ist die payload.
        :return: Länge der Daten in bytes
        """
        pass

    def ermittle_verarbeitungszeit_entwickler_lese(self, startzeit: str, url_zeitstempel: str) -> json:
        """
        Ermittlung startzeit und endzeit mit datetime.utcnow()
        :param startzeit:
        :param url_zeitstempel:
        :return:
        """
        __startzeit: str = startzeit
        __url_zeitstempel: str = url_zeitstempel
        __endzeit: str = ""
        __verarbeitungszeit: str = ""
        __zeitstempel_daten_aus: dict = {}
        zeitstempel_API = API_UF.API(get_request_zulassen = True)
        zeitstempel_API.url_partner = __url_zeitstempel
        if __startzeit == "-1":
            __rueckmeldung_startzeit = zeitstempel_API.hole()
            __startzeit = __rueckmeldung_startzeit["zeitstempel_UTC_original"]
        else:
            __rueckmeldung_endzeit = zeitstempel_API.hole()
            __endzeit = __rueckmeldung_endzeit["zeitstempel_UTC_original"]
            __verarbeitungszeit = __endzeit - __startzeit
        __zeitstempel_daten_aus["startzeit"] = __startzeit
        __zeitstempel_daten_aus["endzeit"] = __endzeit
        __zeitstempel_daten_aus["verarbeitungszeit"] = __verarbeitungszeit

        return json.dumps(__zeitstempel_daten_aus)

    def ermittle_datenstruktur_entwickler_lese(self, daten_speicherobjekt: dict):
        """
        Die Methode ermittelt zu allen Werten des eingehenden Speicherobjektes den entsprechendden Datentyp. Sie soll
        damit Entwicklern schnell Auskunft über die verwendeten Datentypen innerhalb eines Speicherobjektes geben.
        :param daten_speicherobjekt: Schlüssel-Wert-Paare des zu prüfenden Speicherobjekts
        :return: Datentyp für jedes Schlüssel-Wert-Paar
        """
        __daten_speicherobjekt = daten_speicherobjekt
        __daten_speicherobjekt_basisschluessel = __daten_speicherobjekt.keys()
        __daten_speicherobjekt_werte = __daten_speicherobjekt.values()  # Abschneiden des Basisschlüssels
        __datenstruktur_speicherobjekt: dict = {}
        for __schluessel, __werte in __daten_speicherobjekt_werte.items():
            __datenstruktur_speicherobjekt[__schluessel] = type(__werte)
        __datenstruktur_speicherobjekt[__daten_speicherobjekt_basisschluessel] = __datenstruktur_speicherobjekt

        return __datenstruktur_speicherobjekt

    def ermittle_strukturtiefe_baum_entwickler_lese(self):
        """
        Diese Methode ermittelt die Anzahl der Baumebenen, ausgehend von der Wurzel. Dabei wird die Wurzel nicht
        mitgezählt. So erhalten Entwickler Auskunft darüber, aus wie vielen Ebenen die komplette Ressource besteht.
        :return: Anzahl der Ebenen als Integer
        """
        __strukturtiefe: int = 0

        return __strukturtiefe

    def ermittle_datentyp_rueckgabeobjekt_programm_lese(self):
        """
        Die Methode ermittelt den Datentyp des Rückgabeobjekts, z.B. JSON. Dazu wird das Rückgabeobjekt als Parameter
        in die Methode eingesspielt und mithilfe einer type-Abfrage der Datentyp ermittelt.
        :return: Datentyp des Rückgabeobjekts als String
        """
        __datentyp_rueckgabeobjekt: str = ""

        return __datentyp_rueckgabeobjekt

    def rueckmeldung_objekte_fuellen_lese(self):
        pass

    def rueckmeldung_objekte_filtern_lese(self):
        pass


class Persistenz:

    def __init__(self, wurzel: str, datenspeicher = False):
        self.__persistenz_datenspeicher = datenspeicher  # steuert, ob die Daten im Datenspeicher abgelegt werden
        self.datenspeicher: dict = {wurzel: {}}

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
        print("Liste der Hierachien:", __hierarchien)

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

    def lese_speicherinhalt(self, ebenen: list) -> json:  # Ergänzung Parameter: Benutzer-ID, Passwort, Suchschlüssel)
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

    def get_request_in_crud(self, ebenen_ein: list) -> str:
        """
        1. Read
        :return:
        """
        __ebenen: list = ebenen_ein
        __crud_rueckmeldung_get = CRUD_Rueckmeldung()
        __rest_rueckmeldung_get = API_UF.REST_Rueckmeldung()
        __speicherinhalt: dict = {}
        __rueckgaben_daten_aus: dict = {"daten": None,
                                        "rueckmeldung": "",
                                        "fehlercode": 0}

#        __startzeit_crud_rueckmeldung_get = __crud_rueckmeldung_get.ermittle_verarbeitungszeit_entwickler_lese\
#            (startzeit = "-1", url_zeitstempel = "http://localhost:30001/zeitstempel/")["startzeit"]
        __crud_rueckmeldung_get.rueckmeldung_daten["daten"] = json.loads(self.lese_speicherinhalt(__ebenen))
        print("gelesene Daten CRUD", __crud_rueckmeldung_get.rueckmeldung_daten["daten"])
        print("Type CRUD", type(__crud_rueckmeldung_get.rueckmeldung_daten["daten"]))
 #       __verarbeitungszeit_crud_rueckmeldung_get = \
 #           __crud_rueckmeldung_get.ermittle_verarbeitungszeit_entwickler_lese(startzeit = __startzeit_crud_rueckmeldung_get, url_zeitstempel = "http://localhost:30001/zeitstempel/")["verarbeitungszeit"]
 #       __crud_rueckmeldung_get.__rueckmeldung_entwickler["verarbeitungszeit"] = \
 #           __verarbeitungszeit_crud_rueckmeldung_get
        __rueckgaben_daten_aus["daten"] = __crud_rueckmeldung_get.rueckmeldung_daten["daten"]
        print("Type _rueckgabe_daten:", type(__rueckgaben_daten_aus["daten"]))

        print("Rückgabe get_request_in_crud:", json.dumps(__rueckgaben_daten_aus), type(json.dumps(__rueckgaben_daten_aus)))

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
