"""
Das ist die Bibliothek für die Klasse API.
"""

import json
import urllib
import urllib.request
import datetime
from http import HTTPStatus


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
        pass

    def ermittle_status_objekt_nutzer_get(self):
        pass

    def ermittle_laenge_liste_speicherobjekte_nutzer_get(self):
        pass

    def ermittle_startobjekt_nutzer_get(self):
        pass

    def ermittle_laenge_daten_bytes_entwickler_get(self):
        pass

    def ermittle_verarbeitungszeit_entwickler_get(self, startzeit, endzeit):
        """
        Ermittlung startzeit und endzeit mit datetime.utcnow()
        :param startzeit:
        :param endzeit:
        :return:
        """
        __startzeit = startzeit
        __endzeit = endzeit
        __verarbeitungszeit = __endzeit - __startzeit

        return __verarbeitungszeit

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
        self.ressoruce_selbst: str = self.__config["ressource_selbst"]
        self.pfad: str = self.__config["pfad"]
        self.ressource_partner: str = self.__config["ressource_partner"]
        self.url_partner: str = self.__config["url_partner"] + str(self.server_port)
        self.url_partner = ""

    def __encode_daten(self, encode_daten_ein: dict) -> str:
        # Daten werden von Typ Dictionary in JSON-String umgewandelt
        # Encoding-/Decoding-Information aus Config einlesen und If-Bedingung einfügen
        self.__encode_daten_ein = encode_daten_ein
        encode_obj = json.JSONEncoder(sort_keys = False) # KEINE Sortierung der Keys im Bereich der Schnittstelle
        self.__encode_daten_aus = encode_obj.encode(self.__encode_daten_ein)

        return self.__encode_daten_aus

    def __decode_daten(self, decode_daten_ein: str) -> dict:
        # Daten werden vom Typ JSON-String in Dictionary umgewandelt
        # Encoding-/Decoding-Information aus Config einlesen und If-Bedingung einfügen
        self.__decode_daten_ein = decode_daten_ein
        decode_obj = json.JSONDecoder()
        self.__decode_daten_aus = decode_obj.decode(self.__decode_daten_ein)

        return self.__decode_daten_aus

# Methoden zum Empfang von Daten
    def get(self, uebergabedaten_get_ein):
        self.__uebergabedaten_get_ein = uebergabedaten_get_ein

        return self.__uebergabedaten_get_ein

    def post(self, uebergabedaten_post_ein):
        self.__uebergabedaten_post_ein = self.__decode_daten(uebergabedaten_post_ein)

        return self.__uebergabedaten_post_ein

    def put(self, uebergabedaten_put_ein):
        self.__uebergabedaten_put_ein = self.__decode_daten(uebergabedaten_put_ein)

        return self.__uebergabedaten_put_ein

    def patch(self, uebergabedaten_patch_ein):
        self.__uebergabedaten_patch_ein = self.__decode_daten(uebergabedaten_patch_ein)

        return self.__uebergabedaten_patch_ein

    def delete(self, uebergabedaten_delete_ein):
        self.__uebergabedaten_delete_ein = uebergabedaten_delete_ein
        self.__uebergabedaten_delete_ein = json.loads(self.__uebergabedaten_delete_ein)

        return self.__uebergabedaten_delete_ein

# Methoden zum Senden von Daten
    def hole(self, uebergabedaten_hole_aus):
        anfrage_partner = urllib.request.Request(url = self.url_partner, method = "GET")
        self.__uebergabedaten_hole_aus = urllib.request.urlopen(anfrage_partner)
        self.__uebergabedaten_hole_aus = json.load(self.__uebergabedaten_hole_aus)
        print("GET abgeschlossen")

        return self.__uebergabedaten_hole_aus

    def schreibe(self, uebergabedaten_schreibe_aus: dict):
        self.__uebergabedaten_schreibe_aus = self.__encode_daten(uebergabedaten_schreibe_aus)
        self.__uebergabedaten_schreibe_aus = json.dumps(self.__uebergabedaten_schreibe_aus).encode("utf-8")
        anfrage = urllib.request.Request(url = self.url_partner, method = "POST")
        anfrage.add_header("Content-Type", "application/json; charset=utf-8")
        anfrage.add_header("Content-Length", len(self.__uebergabedaten_schreibe_aus))
        urllib.request.urlopen(anfrage, self.__uebergabedaten_schreibe_aus)
        print("POST abgeschlossen")

        return self.__uebergabedaten_schreibe_aus

    def ueberschreibe(self, uebergabedaten_ueberschreibe_aus):
        self.__uebergabedaten_ueberschreibe_aus = self.__encode_daten(uebergabedaten_ueberschreibe_aus)
        self.__uebergabedaten_ueberschreibe_aus = json.dumps(self.__uebergabedaten_ueberschreibe_aus).encode("utf-8")
        anfrage = urllib.request.Request(url = self.url_partner, method = "PUT")
        anfrage.add_header("Content-Type", "application/json; charset=utf-8")
        anfrage.add_header("Content-Length", len(self.__uebergabedaten_ueberschreibe_aus))
        urllib.request.urlopen(anfrage, self.__uebergabedaten_ueberschreibe_aus)
        print("PUT abgeschlossen")

        return self.__uebergabedaten_ueberschreibe_aus

    def aendere(self, uebergabedaten_aendere_aus):
        self.__uebergabedaten_aendere_aus = self.__encode_daten(uebergabedaten_aendere_aus)
        self.__uebergabedaten_aendere_aus = json.dumps(self.__uebergabedaten_aendere_aus).encode("utf-8")
        anfrage = urllib.request.Request(url = self.url_partner, method = "PATCH")
        anfrage.add_header("Content-Type", "application/json; charset=utf-8")
        anfrage.add_header("Content-Length", len(self.__uebergabedaten_aendere_aus))
        urllib.request.urlopen(anfrage, self.__uebergabedaten_aendere_aus)
        print("PATCH abgeschlossen")

        return self.__uebergabedaten_aendere_aus

    def loesche(self, uebergabedaten_loesche_aus):
        self.__uebergabedaten_loesche_aus = self.__encode_daten(uebergabedaten_loesche_aus)
        self.__uebergabedaten_loesche_aus = json.dumps(self.__uebergabedaten_loesche_aus).encode("utf-8")
        anfrage = urllib.request.Request(url = self.url_partner, method = "DELETE")
        anfrage.add_header("Content-Type", "application/json; charset=utf-8")
        anfrage.add_header("Content-Length", len(self.__uebergabedaten_loesche_aus))
        urllib.request.urlopen(anfrage, self.__uebergabedaten_loesche_aus)
        print("DELETE abgeschlossen")

        return self.__uebergabedaten_loesche_aus