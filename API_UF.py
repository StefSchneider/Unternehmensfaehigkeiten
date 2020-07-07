"""
Das ist die Bibliothek für die Klasse API.
"""

import json
import urllib
import urllib.request


ENTWICKLER_INFORMATIONEN: bool = True


class REST_Rueckmeldung:

    def __init__(self, entwickler_informationen_anzeigen: bool = ENTWICKLER_INFORMATIONEN):
        self.__entwickler_informationen_anzeigen = entwickler_informationen_anzeigen
        self.__rueckmeldung:dict = {}
        self.__rueckmeldung_daten: dict = {"daten": None
                                           }
        self.__rueckmeldung_nutzer: dict = {"anzahl_speicherobjekte": None,
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

    def ermittle_speicherinhalt_daten_get(self):
        pass

    def ermittle_anzahl_speicherobjekte_nutzer_get(self):
        # len(dict)
        pass

    def ermittle_status_objekt_nutzer_get(self):
        pass

    def ermittle_laenge_liste_speicherobjekte_nutzer_get(self):
        # derzeit = Anzahl der Speichelemente
        pass

    def ermittle_startobjekt_nutzer_get(self):
        pass

    def ermittle_laenge_daten_bytes_entwickler_get(self):
        pass

    def ermittle_verarbeitungszeit_entwickler_get(self, startzeit: str):
        """
        Ermittlung startzeit und endzeit mit datetime.utcnow()
        :param startzeit:
        :param endzeit:
        :return:
        """
        __startzeit = startzeit
        __endzeit: str = ""
        __verarbeitungszeit: str = ""
        __zeitstempel_daten_aus: dict = {}
        zeitstempel_API = API(get_request_zulassen = True)
        zeitstempel_API.url_partner = "http://localhost:31002/zeitstempel/"
        if __startzeit == -1:
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
        __daten_speicherobjekt_basisschlüssel =  daten_speicherobjekt.keys()
        __daten_speicherobjekt_werte = daten_speicherobjekt.values() # Abschneiden des Basisschlüssels
        __datenstruktur_speicherobjekt: dict = {}
        for __schluessel, __werte in __daten_speicherobjekt_werte.items():
            __datenstruktur_speicherobjekt[__schluessel] = type(__werte)
        __datenstruktur_speicherobjekt[__daten_speicherobjekt_basisschlüssel] = __datenstruktur_speicherobjekt

        return __datenstruktur_speicherobjekt


    def ermittle_strukturtiefe_baum_entwickler_get(self):
        pass

    def ermittle_server_datenquelle_entwickler_get(self):
        pass

    def ermittle_datentyp_rueckgabeobjekt_programm_get(self):
        pass

    def rueckmeldung_objekte_fuellen_get(self):
        """

        :return:
        """
        rueckmeldung_fuer_get_request = self.rueckmeldung_objekte_zusammenfassen()
        rueckmeldung_fuer_get_request = json.dumps(rueckmeldung_fuer_get_request)

        return rueckmeldung_fuer_get_request



    def rueckmeldung_objekte_filtern(self):
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
        self.__rueckmeldung.update(self.__rueckmeldung_daten)
        self.__rueckmeldung.update(self.__rueckmeldung_nutzer)
        self.__rueckmeldung.update(self.__rueckmeldung_programm)
        if self.__entwickler_informationen_anzeigen:
            self.__rueckmeldung.update(self.__rueckmeldung_entwickler)

        return self.__rueckmeldung


class API:

    def __init__(self, get_request_zulassen = False, post_request_zulassen = False, put_request_zulassen = False,
                 patch_request_zulassen = False, delete_request_zulassen = False):
        self.get_request_erlaubt =  get_request_zulassen
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

    def __encode_daten(self, encode_daten_ein: dict) -> bytes:
        """
        Die Methode wandelt die im dict-Format eingehenden Daten in das Format bytes um, damit diese direkt über die
        Schnittstelle als Request gesendet werden können. Zu einem späteren Zeitpunkt können die Daten auch in andere
        Formate umgewandelt werden. Das Format könnte entweder über die Config-Datei gesetzt werden oder über einen
        Parameter. Um mehrere Format zu behandeln, sollten diese über If-Bedingungen innerhalb der Methode gesteuert
        werden.
        :param encode_daten_ein: Daten, die für den Request kodiert werden sollen
        :return: codierte Daten
        """
        __encode_daten_ein: dict = encode_daten_ein
        __encode_daten_ein: json = json.dumps(__encode_daten_ein) # Umwandlung in JSON-String
        __encode_daten_ein: bytes = __encode_daten_ein.encode("utf-8") # Umwandlung in Bytes
        __encode_daten_aus: bytes = __encode_daten_ein

        return __encode_daten_aus

    def __decode_daten(self, decode_daten_ein: bytes) -> dict:
        """
        Die Methode wandet eingehende Daten Format Bytes in ein Dictionary um. Sollte die Umwandlung in weitere
        Datenformate gewünscht werden, könnte dies über eine If-Bedingung gesteuert werden. Das im Einzelfall benötigte
        Datenformat könnte über die Config-Datei gesetzt werden oder als Parameter in die Methode gegeben werden.
        :param decode_daten_ein: umzuwandelnde Daten
        :return: in ein Dictionary dekodierte Daten
        """
        __decode_daten_ein: bytes = decode_daten_ein
        __decode_daten_ein: json = __decode_daten_ein.decode() # Umwandlung in JSON-String
        __decode_daten_ein: dict = json.loads(decode_daten_ein) # Umwandlung in Dictionary
        __decode_daten_aus: dict = __decode_daten_ein

        return __decode_daten_aus

# Methoden zum Empfang von Daten
    def get(self, uebergabedaten_get_ein: bytes) -> bytes:
        __uebergabedaten_get_ein: bytes = uebergabedaten_get_ein
        __uebergabedaten_get_aus: bytes = __uebergabedaten_get_ein

        return __uebergabedaten_get_aus

    def post(self, uebergabedaten_post_ein: bytes) -> dict:
        __uebergabedaten_post_ein: bytes = uebergabedaten_post_ein
        __uebergabedaten_post_ein: dict = self.__decode_daten(__uebergabedaten_post_ein)
        __uebergabedaten_post_aus: dict = __uebergabedaten_post_ein

        return __uebergabedaten_post_aus

    def put(self, uebergabedaten_put_ein: bytes) -> dict:
        __uebergabedaten_put_ein: bytes = uebergabedaten_put_ein
        __uebergabedaten_put_ein: dict = self.__decode_daten(__uebergabedaten_put_ein)
        __uebergabedaten_put_aus: dict = __uebergabedaten_put_ein

        return __uebergabedaten_put_aus

    def patch(self, uebergabedaten_patch_ein: bytes) -> dict:
        __uebergabedaten_patch_ein: bytes = uebergabedaten_patch_ein
        __uebergabedaten_patch_ein: dict = self.__decode_daten(__uebergabedaten_patch_ein)
        __uebergabedaten_patch_aus: dict = __uebergabedaten_patch_ein

        return __uebergabedaten_patch_aus

    def delete(self, uebergabedaten_delete_ein):
        self.__uebergabedaten_delete_ein = uebergabedaten_delete_ein
        self.__uebergabedaten_delete_aus = self.__uebergabedaten_delete_ein

        return self.__uebergabedaten_delete_aus

# Methoden zum Senden von Daten
    def hole(self) -> json:
#        self.__uebergabedaten_hole_ein = uebergabedaten_hole_ein | keine Parameter uebergabedaten nötig
        __anfrage_partner = urllib.request.Request(url = self.url_partner, method = "GET")
        __uebergabedaten_hole_aus = urllib.request.urlopen(__anfrage_partner)
        __uebergabedaten_hole_aus = __uebergabedaten_hole_aus.read()
        __uebergabedaten_hole_aus = self.__decode_daten(__uebergabedaten_hole_aus)
        print("GET abgeschlossen")

        return __uebergabedaten_hole_aus

    def schreibe(self, uebergabedaten_schreibe_ein: dict) -> json:
        """
        Umwandlung der Daten erfolgt über die Methode __encode, damit kann das zu verarbeitende Datenformat jederzeit
        über die Methode schnell angepasst werden, ohne in allen Funktionen erneuert werden zu müssen.
        ACHTUNG: Datenformat über daten_typ_inhalt muss zum Format in der Methode __encode passen
        :param uebergabedaten_schreibe_ein: Daten, die mit dem POST-Request mitgeschickt werden
        :return: die über den POST-Request mitgeschickten Daten für die Ressource
        """
        __uebergabedaten_schreibe_aus = self.__encode_daten(uebergabedaten_schreibe_ein)
        __anfrage_partner = urllib.request.Request(url = self.url_partner, method = "POST")
        __anfrage_partner.add_header("Content-Type", self.daten_typ_inhalt)
        __anfrage_partner.add_header("Content-Length", len(__uebergabedaten_schreibe_aus))
        urllib.request.urlopen(__anfrage_partner, __uebergabedaten_schreibe_aus)
        print("POST abgeschlossen")

        return __uebergabedaten_schreibe_aus

    def ueberschreibe(self, uebergabedaten_ueberschreibe_ein):
        """
        Umwandlung der Daten erfolgt über die Methode __encode, damit kann das zu verarbeitende Datenformat jederzeit
        über die Methode schnell angepasst werden, ohne in allen Funktionen erneuert werden zu müssen.
        ACHTUNG: Datenformat über daten_typ_inhalt muss zum Format in der Methode __encode passen
        :param uebergabedaten_ueberschreibe_ein: Daten, die mit dem PUT-Request mitgeschickt werden
        :return: die über den PUT-Request mitgeschickten Daten für die Ressource
        """
        self.__uebergabedaten_ueberschreibe_aus = self.__encode_daten(uebergabedaten_ueberschreibe_ein)
        __anfrage_partner = urllib.request.Request(url = self.url_partner, method = "PUT")
        __anfrage_partner.add_header("Content-Type", self.daten_typ_inhalt)
        __anfrage_partner.add_header("Content-Length", len(self.__uebergabedaten_ueberschreibe_aus))
        urllib.request.urlopen(__anfrage_partner, self.__uebergabedaten_ueberschreibe_aus)
        print("PUT abgeschlossen")

        return self.__uebergabedaten_ueberschreibe_aus

    def aendere(self, uebergabedaten_aendere_ein):
        """
        Umwandlung der Daten erfolgt über die Methode __encode, damit kann das zu verarbeitende Datenformat jederzeit
        über die Methode schnell angepasst werden, ohne in allen Funktionen erneuert werden zu müssen.
        ACHTUNG: Datenformat über daten_typ_inhalt muss zum Format in der Methode __encode passen
        :param uebergabedaten_aendere_ein: Daten, die mit dem PATCH-Request mitgeschickt werden
        :return: die über den PATCH-Request mitgeschickten Daten für die Ressource
        """
        self.__uebergabedaten_aendere_aus = self.__encode_daten(uebergabedaten_aendere_ein)
        __anfrage_partner = urllib.request.Request(url = self.url_partner, method = "PATCH")
        __anfrage_partner.add_header("Content-Type", self.daten_typ_inhalt)
        __anfrage_partner.add_header("Content-Length", len(self.__uebergabedaten_aendere_aus))
        urllib.request.urlopen(__anfrage_partner, self.__uebergabedaten_aendere_aus)
        print("PATCH abgeschlossen")

        return self.__uebergabedaten_aendere_aus

    def loesche(self):
#        self.__uebergabedaten_loesche_aus = self.__encode_daten(uebergabedaten_loesche_ein) | keine Parameter uebergabedaten nötig
        __anfrage_partner = urllib.request.Request(url = self.url_partner, method = "DELETE")
        urllib.request.urlopen(__anfrage_partner)
        print("DELETE abgeschlossen")

        return "OK"