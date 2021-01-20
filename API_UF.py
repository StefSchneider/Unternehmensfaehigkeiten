"""
Das ist die Bibliothek für die Klasse API.
"""

import json
import urllib
import urllib.request
from urllib.request import Request

from flask import request


ENTWICKLER_INFORMATIONEN: bool = True
# Die Konstate steuert zunächst, ob Daten für Entwickler angezeigt werden, ist für die Programmierung sinnvoll,
# sollte später nur in besonderen Fällen aktiviert werden. Die Steuerung soll später über entsprechende Einträge in
# Config-Datein erfolgen.


class REST_Rueckmeldung:

    def __init__(self, entwickler_informationen_anzeigen: bool = ENTWICKLER_INFORMATIONEN):
        """
        In dieser Klasse werden die Daten sowohl aus der Ressource als auch Zusatzdaten, die auf Basis der Ressource
        enstehen, abgespeichert und erfasst. Diese Daten entstehen und werden verarbeitet zum Zeitpunkt des Aufrufes
        der REST Api. Grundsätzlich sind vier Datenbereiche interessant:
        1. Die Kerndaten, die in der Ressource abgespeichert sind. (Kennzeichnung: "_daten")
        2. Daten, die für Nutzer bei der späteren Anwendung interessant sind. (Kennzeichen: "_nutzer")
        3. Daten, die für Entwickler interessant sind. (Kennzeichen: "_entwickler")
        4. Daten zum Programm an sich. (Kennzeichen: "_programm")
        Alle vier Bereiche verfügen über ein eigenes Dictionary, in dem die Daten abgelegt werden. Sie werden in einem
        Gesamtdictionary self.__rueckmeldung aggregiert. Alle Dictionaries werden bei der Anlage einer enstprechenden
        Instanz angelegt.
        :param entwickler_informationen_anzeigen:
        """
        self.__entwickler_informationen_anzeigen = entwickler_informationen_anzeigen
        self.__rueckmeldung: dict = {}
        self.__rueckmeldung_daten: dict = {"daten": None
                                           }
        self.__rueckmeldung_nutzer: dict = {"anzahl_speicherobjekte": 0,
                                            "status": None,
                                            "anzahl_rueckgabeobjekte": None,
                                            "startobjekt": 0
                                            }
        self.__rueckmeldung_entwickler: dict = {"laenge_bytes": None,
                                                "verarbeitungszeit": None,
                                                "datenstruktur": None,
                                                "strukturtiefe": None,
                                                "server_datenquelle": None
                                                }
        self.__rueckmeldung_programm: dict = {"datentyp_rueckgabeobjekt": None
                                              }
        self.__rueckmeldung_fuer_get_request: dict = {}

    def ermittle_speicherinhalt_daten_get(self):
        """
        Die Methode liefert den Inhalt des Speicherobjekts (payload) bei einem GET-Request zurück. Die Daten werden aus
        der Abfrage innerhalb der Persistenz übernommen.
        :return: Inhalt der Ressource
        """
        pass

    def ermittle_anzahl_speicherobjekte_nutzer_get(self):
        """
        Die Methode ermittelt die Anzahl der Speicherobjekte zum angefragten Schlüssel. Dabei wird nur die erste
        Hierarchiestufe abgefragt, aber keine Unter-Dictionaries. Damit kann der Nutzer erkennen, wie viele Objekte
        in der Ressource, die er abfragt, abgespeichert sind. Er kann dann entscheiden, ob er seine Abfrage einschränkt,
        um weniger Daten zu erhalten. Die Berechnung erfolgt auf Basis der payload und wird hier erneut
        durchgeführt, unabhängig vom Ergebnis der gleichen Berechnung in der Persistenz.
        :return: Anzahl der Speicherobjekte als Integer
        """
        # len(dict)
        pass

    def ermittle_status_objekt_nutzer_get(self):
        """
        Die Methode ermittelt, ob die angefragte Speicherobjekt überhaupt vorhanden ist. Basis sind die Daten der
        Rückmeldung aus der Persistenz.
        :return: Dictionary mit Einträgen True/False (bool) und "Ressource vorhanden"/"Ressource nicht vorhanden" (str)
        """
        pass

    def ermittle_laenge_liste_speicherobjekte_nutzer_get(self):
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

    def ermittle_startobjekt_nutzer_get(self):
        """
        Diese Methode ermittelt das vom Nutzer vorgegebene Startobjekt innerhalb der Liste der zurückgegebenen
        Speicherobjekte. Diese Methode ist später einsetzbar, wenn ein Nutzer die Daten der Ressource erst ab einem
        bestimmten Punkt sehen möchte, z.B. erst ab Objekt "xyz" aufwärts. Zunächst ist das Startobjekt immer 0. Die
        Berechnung erfolgt auf Basis der payload und wird unabhängig von der Berechnung innerhalb der Persistenz
        durchgeführt.
        :return: Position des Startobjekts in der Gesamtliste als int
        """
        pass

    def ermittle_laenge_daten_bytes_entwickler_get(self):
        """
        Die Methode ermittelt die Größe der payload in Byte. Grundlage für die Berechnung ist die payload, die
        Berechnung wird unabhängig von der Berechnung innerhalb der Persistenz durchgeführt.
        :return: Länge der Daten in bytes
        """
        pass

    def ermittle_verarbeitungszeit_entwickler_get(self, startzeit: str, url_zeitstempel: str) -> json:
        """
        Die Methode ermittelt die Zeitspanne zwischen dem Beginn und dem Ende der Ressourcenabfrage. Das Ende ist
        mit der Rückgabe der payload erreicht. Wir die Methode mit der Startzeit "-1" aufgerufen, ermittelt sie den
        Zeitstempel zu Beginn der Abfrage; wird die Methode mit einer richtigen Startzeit aufgerufen, ermittelt sie die
        Endzeit und die daras resultierende Zeitspanne.
        Ermittlung startzeit und endzeit mit datetime.utcnow()
        :param startzeit: vorher ermittelte Startzeit oder "-1" als str
        :param url_zeitstempel: URL, über die der Zeitstempel abgeholt werden kann (Microservice) als str
        :return: Zeitdaten, d.h. Startzeit, Endzeit und Verarbeitungszeit als str
        """
        __startzeit: str = startzeit
        __url_zeitstempel: str = url_zeitstempel
        __endzeit: str = ""
        __verarbeitungszeit: str = ""
        __zeitstempel_daten_aus: dict = {}
        zeitstempel_API = API(get_request_zulassen = True)
        zeitstempel_API.url_partner = __url_zeitstempel
        if __startzeit == "-1":
            __startzeit = zeitstempel_API.hole()
            __startzeit = __startzeit["zeitstempel_UTC_original"]
        else:
            __endzeit = zeitstempel_API.hole()
            __endzeit = __endzeit["zeitstempel_UTC_original"]
            __verarbeitungszeit = __endzeit - __startzeit
        __zeitstempel_daten_aus["startzeit"] = __startzeit
        __zeitstempel_daten_aus["endzeit"] = __endzeit
        __zeitstempel_daten_aus["verarbeitungszeit"] = __verarbeitungszeit

        return json.dumps(__zeitstempel_daten_aus)

    def ermittle_datenstruktur_entwickler_get(self, daten_speicherobjekt: dict):
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

    def ermittle_strukturtiefe_baum_entwickler_get(self):
        """
        Diese Methode ermittelt die Anzahl der Baumebenen, ausgehend von der Wurzel. Dabei wird die Wurzel nicht
        mitgezählt. So erhalten Entwickler Auskunft darüber, aus wie vielen Ebenen die komplette Ressource besteht.
        :return: Anzahl der Ebenen als Integer
        """
        __strukturtiefe: int = 0

        return __strukturtiefe

    def ermittle_server_datenquelle_entwickler_get(self):
        """
        Die Methode ermittelt, welcher Server den GET-Request beantwortet, also welche Datenquelle aktiv ist. Derzeit
        ist es nur eine Konstante, die zurückgegeben wird, d.h. der eigene Rechner, z.B. localhost: , also die IP-
        Adresse ohne Port.
        :return: Name des Servers, der die Daten bereitstellt als String
        """
        __servername_datenquelle: str = ""

        return __servername_datenquelle

    def ermittle_datentyp_rueckgabeobjekt_programm_get(self):
        """
        Die Methode ermittelt den Datentyp des Rückgabeobjekts, z.B. JSON. Dazu wird das Rückgabeobjekt als Parameter
        in die Methode eingesspielt und mithilfe einer type-Abfrage der Datentyp ermittelt.
        :return: Datentyp des Rückgabeobjekts als String
        """
        __datentyp_rueckgabeobjekt: str = ""

        return __datentyp_rueckgabeobjekt

    def rueckmeldung_objekte_fuellen_get(self):
        """

        :return:
        """
        self.__rueckmeldung_fuer_get_request: dict = {}
        self.__rueckmeldung_fuer_get_request.update(self.__rueckmeldung_daten)
        self.__rueckmeldung_fuer_get_request.update(self.__rueckmeldung_nutzer)
        self.__rueckmeldung_fuer_get_request.update(self.__rueckmeldung_entwickler)
        self.__rueckmeldung_fuer_get_request.update(self.__rueckmeldung_programm)

        return self.__rueckmeldung_fuer_get_request

    def rueckmeldung_objekte_filtern_get(self):
        """
        NEU PROGRAMMIEREN ALS FILTER
        "daten" fällt weg, wenn die Ressource nicht vorhanden ist
        "entwickler fällt weg, Entwickler-Infos ausgeschaltet sind
        ------
        Die Methode fasst die einzelnen Dictionaries zu einem Dictionary zusammen, dabei filtert sie nicht gewünschte
        Rückgabeobjekte heraus. Anschließend wandelt die Rückgabeinformationen in ein JSON-Format um.
        Die Informationen, die Entwickler betreffen, sollen zuschaltbar sein, wenn das entsprechende Attribut True ist.
        :return: Zusammenstellung der Rückgabeinformationen für Daten, Nutzer, Programm und möglicherweise Entwickler
        """

        if not self.__entwickler_informationen_anzeigen:
            del self.__rueckmeldung_fuer_get_request[self.__rueckmeldung_entwickler]
        self.__rueckmeldung_fuer_get_request = json.dumps(self.__rueckmeldung_fuer_get_request)

        return self.__rueckmeldung_fuer_get_request


class API:

    def __init__(self, get_request_zulassen = False, post_request_zulassen = False, put_request_zulassen = False,
                 patch_request_zulassen = False, delete_request_zulassen = False):
        """

        :param get_request_zulassen: steuert, ob per GET-Request auf den Microservice zugegriffen werden darf
        :param post_request_zulassen: steuert, ob per POST-Request auf den Microservice zugegriffen werden darf
        :param put_request_zulassen: steuert, ob per PUT-Request auf den Microservice zugegriffen werden darf
        :param patch_request_zulassen: steuert, ob per PATCH-Request auf den Microservice zugegriffen werden darf
        :param delete_request_zulassen: steuert, ob per DELETE-Request auf den Microservice zugegriffen werden darf
        """
        self.get_request_erlaubt = get_request_zulassen
        self.post_request_erlaubt = post_request_zulassen
        self.put_request_erlaubt = put_request_zulassen
        self.patch_request_erlaubt = patch_request_zulassen
        self.delete_request_erlaubt = delete_request_zulassen
        self.__config: dict = {"server_port": 30010,
                               "ressource_selbst": "/hello",
                               "pfad": "/",
                               "ressource_partner": "/print",
                               "url_partner": "localhost:"
                               }
        self.server_port: int = self.__config["server_port"]
        self.ressource_selbst: str = self.__config["ressource_selbst"]
        self.pfad: str = self.__config["pfad"]
        self.ressource_partner: str = self.__config["ressource_partner"]
        self.url_partner: str = self.__config["url_partner"] + str(self.server_port)
        self.url_partner = ""
        self.daten_typ_inhalt: str = "application/json; charset=utf-8"

    def __encode_daten(self, encode_daten: dict) -> bytes:
        """
        Die Methode wandelt die im dict-Format eingehenden Daten in das Format bytes um, damit diese direkt über die
        Schnittstelle als Request gesendet werden können. Zu einem späteren Zeitpunkt können die Daten auch in andere
        Formate umgewandelt werden. Das Format könnte entweder über die Config-Datei gesetzt werden oder über einen
        Parameter. Um mehrere Format zu behandeln, sollten diese über If-Bedingungen innerhalb der Methode gesteuert
        werden.
        :param encode_daten: Daten, die für den Request kodiert werden sollen
        :return: codierte Daten
        """
        __encode_daten_ein: dict = encode_daten
        __encode_daten_verarbeitung: json = ""
        __encode_daten_aus: bytes = b''
        __encode_daten_verarbeitung = json.dumps(__encode_daten_ein)  # Umwandlung in JSON-String
        __encode_daten_aus = __encode_daten_verarbeitung.encode("utf-8")  # Umwandlung in Bytes

        return __encode_daten_aus

    def __decode_daten(self, decode_daten: bytes) -> dict:
        """
        Die Methode wandet eingehende Daten Format Bytes in ein Dictionary um. Sollte die Umwandlung in weitere
        Datenformate gewünscht werden, könnte dies über eine If-Bedingung gesteuert werden. Das im Einzelfall benötigte
        Datenformat könnte über die Config-Datei gesetzt werden oder als Parameter in die Methode gegeben werden.
        :param decode_daten: umzuwandelnde Daten
        :return: in ein Dictionary dekodierte Daten
        """
        __decode_daten_ein: bytes = decode_daten
        __decode_daten_verarbeitung: json = ""
        __decode_daten_aus: dict = {}
        __decode_daten_verarbeitung = __decode_daten_ein.decode()  # Umwandlung in JSON-String
        __decode_daten_aus = json.loads(__decode_daten_verarbeitung)  # Umwandlung in Dictionary

        return __decode_daten_aus

# Methoden zum Empfang von Daten:

    def get(self, uebergabedaten_get: bytes) -> bytes:
        """
        Auf eine Decodierung kann verzichtet werden, da die Methode die Daten aus Typ Bytes erhält und auch als Typ
        Bytes zurückliefert.
        :param uebergabedaten_get:
        :return:
        """
        __uebergabedaten_get_ein: bytes = uebergabedaten_get
        __uebergabedaten_get_aus: bytes = b''
        __uebergabedaten_get_aus = __uebergabedaten_get_ein

        return __uebergabedaten_get_aus

#    def post(self, uebergabedaten_post: bytes) -> dict:
    def post(self) -> dict:

        """

        :param uebergabedaten_post:
        :return:
        """
        __daten = request.data
#       __uebergabedaten_post_ein: bytes = uebergabedaten_post
        __uebergabedaten_post_aus: dict = {}
#        __uebergabedaten_post_aus: dict = self.__decode_daten(__uebergabedaten_post_ein)
        __uebergabedaten_post_aus = self.__decode_daten(__daten)

        return __uebergabedaten_post_aus

    def put(self, uebergabedaten_put: bytes) -> dict:
        """

        :param uebergabedaten_put:
        :return:
        """
        __uebergabedaten_put_ein: bytes = uebergabedaten_put
        __uebergabedaten_put_aus: dict = {}
        __uebergabedaten_put_aus = self.__decode_daten(__uebergabedaten_put_ein)

        return __uebergabedaten_put_aus

    def patch(self, uebergabedaten_patch: bytes) -> dict:
        """

        :param uebergabedaten_patch:
        :return:
        """
        __uebergabedaten_patch_ein: bytes = uebergabedaten_patch
        __uebergabedaten_patch_aus: dict = {}
        __uebergabedaten_patch_aus = self.__decode_daten(__uebergabedaten_patch_ein)

        return __uebergabedaten_patch_aus

    def delete(self, uebergabedaten_delete: bytes) -> dict:
        """

        :param uebergabedaten_delete:
        :return:
        """
        __uebergabedaten_delete_ein: bytes = uebergabedaten_delete
        __uebergabedaten_delete_aus: dict = {}
        __uebergabedaten_delete_aus = self.__decode_daten(__uebergabedaten_delete_ein)

        return __uebergabedaten_delete_aus

# Methoden zum Senden von Daten:

    def hole(self) -> dict:
        """
        Die Methode startet einen GET-Request beim Microservice der den Inhalt der Ressource bereithält. Bei der Methode
        müssen keine Daten als Parameter mitgeliefert werden. Die Methode verändert die Ressource/das Speicherobjekt
        nicht. Auf welche Ressource der GET-Request angewendet werden soll, ergibt sich aus dem angesprochenen Pfad im
        jeweiligen Microservice.
        :return: Die Daten, die von den angeforderten Ressource zurückgeliefert wurden als Dict
        """
        __rueckgabedaten_requestpartner: bytes = b""
        __rueckgabedaten_hole: dict = {}
        __request_an_partner: Request = urllib.request.Request(url = self.url_partner, method = "GET")
        __request_an_partner = urllib.request.urlopen(__request_an_partner)
        __rueckgabedaten_request_partner: bytes = __request_an_partner.read()
        # liest die vom Partner zurückgelieferten Daten ein
        __rueckgabedaten_hole: dict = self.__decode_daten(__rueckgabedaten_requestpartner)
        print("GET abgeschlossen")

        return __rueckgabedaten_hole

    def schreibe(self, uebergabedaten_schreibe: dict) -> bytes:
        """
        Die Methode startet einen POST-Request beim Microservice der den Inhalt der Ressource bereithält. Als Parameter
        werden die Daten übergeben, die die neue Ressource/das neue Speicherobjekt aufnehmen soll. Die Umwandlung der
        Daten erfolgt über die Methode __encode, damit kann das zu verarbeitende Datenformat jederzeit über die Methode
        schnell angepasst werden, ohne in allen Methoden erneuert werden zu müssen.
        ACHTUNG: Das Datenformat über daten_typ_inhalt muss zum Format in der Methode __encode passen
        :param uebergabedaten_schreibe: Daten, die die neue Ressource aufnehmen soll
        :return: die über den POST-Request mitgeschickten Daten für die Ressource
        """
        __uebergabedaten_ein: dict = uebergabedaten_schreibe
        __uebergabedaten_request: bytes = b""
        __rueckgabedaten_schreibe: bytes = b""
        __uebergabedaten_request = self.__encode_daten(__uebergabedaten_ein)
        __request_an_partner: Request = urllib.request.Request(url = self.url_partner, method = "POST")
        __request_an_partner.add_header("Content-Type", self.daten_typ_inhalt)
        __request_an_partner.add_header("Content-Length", str(len(__uebergabedaten_request)))
        urllib.request.urlopen(__request_an_partner, __uebergabedaten_request)
        __rueckgabedaten_schreibe = __uebergabedaten_request
        print("POST abgeschlossen")

        return __rueckgabedaten_schreibe

    def ueberschreibe(self, uebergabedaten_ueberschreibe: dict) -> bytes:
        """
        Die Methode startet einen PUT-Request beim Microservice der den Inhalt der Ressource bereithält. Als Parameter
        werden die Daten übergeben, mit der die angesprochene Ressource/das Speicherobjekt überschrieben werden soll.
        Dabei wird der komplette Inhalt überschrieben. Die Umwandlung der Daten erfolgt über die Methode __encode, damit
        kann das zu verarbeitende Datenformat jederzeit über die Methode schnell angepasst werden, ohne in allen
        Methoden erneuert werden zu müssen.
        ACHTUNG: Das Datenformat über daten_typ_inhalt muss zum Format in der Methode __encode passen
        :param uebergabedaten_ueberschreibe: Daten, mit der die Ressource überschrieben werden soll
        :return: die über den PUT-Request mitgeschickten Daten für die Ressource
        """
        __uebergabedaten_ein: dict = uebergabedaten_ueberschreibe
        __uebergabedaten_request: bytes = b""
        __rueckgabedaten_ueberschreibe: bytes = b""
        __uebergabedaten_request = self.__encode_daten(__uebergabedaten_ein)
        __request_an_partner: Request = urllib.request.Request(url = self.url_partner, method = "PUT")
        __request_an_partner.add_header("Content-Type", self.daten_typ_inhalt)
        __request_an_partner.add_header("Content-Length", str(len(__uebergabedaten_request)))
        urllib.request.urlopen(__request_an_partner, __uebergabedaten_request)
        __rueckgabedaten_ueberschreibe = __uebergabedaten_request
        print("PUT abgeschlossen")

        return __rueckgabedaten_ueberschreibe

    def aendere(self, uebergabedaten_aendere: dict) -> bytes:
        """
        Die Methode startet einen PATCH-Request beim Microservice der den Inhalt der Ressource bereithält. Als Parameter
        werden die Daten übergeben, die bei der angesprochenen Ressource/dem Speicherobjekt überschrieben werden sollen.
        Dabei werden nur die Teile des Inhalt geändert, die überschrieben werden sollen. Die Umwandlung der Daten
        erfolgt über die Methode __encode, damit kann das zu verarbeitende Datenformat jederzeit über die Methode
        schnell angepasst werden, ohne in allen Methoden erneuert werden zu müssen.
        ACHTUNG: Das Datenformat über daten_typ_inhalt muss zum Format in der Methode __encode passen
        :param uebergabedaten_aendere: Daten, die bei der Ressource geändert werden sollen
        :return: die über den PATCH-Request mitgeschickten Daten für die Ressource
        """
        __uebergabedaten_ein: dict = uebergabedaten_aendere
        __uebergabedaten_request: bytes = b""
        __rueckgabedaten_aendere: bytes = b""
        __uebergabedaten_request = self.__encode_daten(__uebergabedaten_ein)
        __request_an_partner: Request = urllib.request.Request(url = self.url_partner, method = "PATCH")
        __request_an_partner.add_header("Content-Type", self.daten_typ_inhalt)
        __request_an_partner.add_header("Content-Length", str(len(__uebergabedaten_request)))
        urllib.request.urlopen(__request_an_partner, __uebergabedaten_request)
        __rueckgabedaten_aendere = __uebergabedaten_request
        print("PATCH abgeschlossen")

        return __rueckgabedaten_aendere

    def loesche(self) -> str:
        """
        Die Methode startet einen DELETE-Request beim Microservice der den Inhalt der Ressource bereithält. Damit wird
        die gesamte Resource/das Speicherobjekt gelöscht. Die Umwandlung der (Leer-)Daten erfolgt über die Methode
        __encode, damit kann das zu verarbeitende Datenformat jederzeit über die Methode schnell angepasst werden, ohne
        in allen Methoden erneuert werden zu müssen.
        ACHTUNG: Das Datenformat über daten_typ_inhalt muss zum Format in der Methode __encode passen
        :return: "OK"
        """
        __uebergabedaten_leer: dict = {}
        # Der Request benötigt im Header mitzuliefernde Daten. Da die Methode nicht den Inhalt des Speicherobjekts
        # ändert, wird ein leeres Dictionary eingesetzt
        __uebergabedaten_request: bytes = b""
        __rueckgabedaten_loesche: str = ""
        __uebergabedaten_request = self.__encode_daten(__uebergabedaten_leer)
        __request_an_partner: Request = urllib.request.Request(url = self.url_partner, method = "DELETE")
        __request_an_partner.add_header("Content-Type", self.daten_typ_inhalt)
        __request_an_partner.add_header("Content-Length", str(len(__uebergabedaten_request)))
        urllib.request.urlopen(__request_an_partner, __uebergabedaten_request)
        __rueckgabedaten_loesche = "OK"
        print("DELETE abgeschlossen")

        return __rueckgabedaten_loesche
