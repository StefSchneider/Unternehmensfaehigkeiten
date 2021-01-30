import json
import urllib
from urllib.request import Request
from flask import request
import API_UF


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
