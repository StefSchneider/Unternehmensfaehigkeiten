"""
Das ist die Bibliothek für die Klasse API.
"""

import json
import urllib
from urllib.request import Request
from flask import request


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

    @staticmethod
    def __encode_daten(encode_daten: dict) -> bytes:
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

    @staticmethod
    def __decode_daten(decode_daten: bytes) -> dict:
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
        with urllib.request.urlopen(__request_an_partner) as __antwort:
            __rueckgabedaten_requestpartner = __antwort.read()  # liest die vom Partner zurückgelieferten Daten ein
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

# Methoden zum Empfangen von Daten:

    def get(self) -> dict:
        """
        Die Methode nimmt den GET-Request des Empfängers auf und übersetzt die mitgelieferten Daten in das passende
        Format zur weiteren Verarbeitung.
        ACHTUNG: Derzeit erfolgt bei einem GET-Request keine zusätzliche Datenübermittlung
        :return: Die vom GET-Request übergebenen Daten als Tabelle
        """
        __eingangsdaten_request: bytes = b""
        __rueckgabedaten_get: dict = {}
        __eingangsdaten_request = request.data
        __rueckgabedaten_get = self.__decode_daten(__eingangsdaten_request)

        return __rueckgabedaten_get

    def post(self) -> dict:
        """
        Die Methode nimmt den POST-Request des Empfängers auf und übersetzt die mitgelieferten Daten in das passende
        Format zur weiteren Verarbeitung.
        :return: Die vom POST-Request übergebenen Daten als Tabelle
        """
        __eingangsdaten_request: bytes = b""
        __rueckgabedaten_post: dict = {}
        __eingangsdaten_request = request.data
        __rueckgabedaten_post = self.__decode_daten(__eingangsdaten_request)

        return __rueckgabedaten_post

    def put(self) -> dict:
        """
        Die Methode nimmt den PUT-Request des Empfängers auf und übersetzt die mitgelieferten Daten in das passende
        Format zur weiteren Verarbeitung.
        :return: Die vom PUT-Request übergebenen Daten als Tabelle
        """
        __eingangsdaten_request: bytes = b""
        __rueckgabedaten_put: dict = {}
        __eingangsdaten_request = request.data
        __rueckgabedaten_put = self.__decode_daten(__eingangsdaten_request)

        return __rueckgabedaten_put

    def patch(self) -> dict:
        """
        Die Methode nimmt den PATCH-Request des Empfängers auf und übersetzt die mitgelieferten Daten in das passende
        Format zur weiteren Verarbeitung.
        :return: Die vom PATCH-Request übergebenen Daten als Tabelle
        """
        __eingangsdaten_request: bytes = b""
        __rueckgabedaten_patch: dict = {}
        __eingangsdaten_request = request.data
        __rueckgabedaten_patch = self.__decode_daten(__eingangsdaten_request)

        return __rueckgabedaten_patch

    def delete(self) -> dict:
        """
        Die Methode nimmt den DELETE-Request des Empfängers auf und übersetzt die mitgelieferten Daten in das passende
        Format zur weiteren Verarbeitung.
        :return: Die vom DELETE-Request übergebenen Daten als Tabelle
        """
        __eingangsdaten_request: bytes = b""
        __rueckgabedaten_delete: dict = {}
        __eingangsdaten_request = request.data
        __rueckgabedaten_delete = self.__decode_daten(__eingangsdaten_request)

        return __rueckgabedaten_delete
