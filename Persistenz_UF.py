"""
Das ist die Bibliothek der Klasse Persistenz
"""

import json
import random
import collections


class Speicherinhalt:

    def __init__(self):
        self.speicherelement: dict = {}

    def __str__(self):

        return str(self.speicherelement)

    def __repr__(self):

        return str(self.speicherelement)


class Speicherdaten:

    def __init__(self):
        self.schluessel: str = ""
        self.speicherinhalt = Speicherinhalt()

    def __repr__(self):

        return str(self.schluessel)


class Baum:

    def __init__(self):
        self.speicherdaten = Speicherdaten()
        self.kinder: list = []
        self.elternpfad: list = []

    def __repr__(self):

        return str(self.speicherdaten)

    def wandle_baum_in_dict(self) -> dict:
        """
        Diese Methode wandelt die Baumstruktur der Persistenz in ein Dictionary um, damit dieses später im JSON-Format
        übertragen werden kann. Dazu werden der Reihe nach alle Speicherobjekte im Baum durchlaufen und in eine
        Queue geschrieben, bis das letzte Objekt eines Pfads erreicht ist (die Variable kinder enthält eine leere
        Liste). Der Vorteil der Speicherung von Objekten in der Queue besteht darin, dass sobald das Pfadende erreicht
        ist, der Baum nicht wieder von oben durchlaufen werden muss - anders als beim Dictionary. Die Methode endet,
        wenn kein Objekt mehr in der Queue liegt, d.h. alle Objekte abgearbeitet wurden. Es müssen zwei Pfade gesteuert
        werden: der Pfad durch den Baum und der Pfad durch das Dictionary. Die Speicherinhalte werden als eigene Klasse
        (Speicherinhalt) im Dictionary gespeichert, um bei anderen Methoden, die ein entsprechendes Dictionary
        analysieren, ein Ende des Pfades zu markieren, d.h. der Eintrag Speicherinhalt in einem Dictionary das Ende,
        das die Speicherdaten enthält.
        :return: den umgewandelten Baum als dict
        """
        print("IN WANDLE BAUM")
        __aktuelles_speicherobjekt_baum = self
        __dictionary_aus_baum: dict = {}  # Gesamt-Dictionary, das ausgefüllt zurückgegeben wird
        __aktueller_teil_dictionary: dict = {}  # der Teil des Dictionaries, der aktualisiert werden muss
        # Damit beim Update des Dictionaries die Ergänzung um das aktuelle Speicherdaten nur auf der entsprechenden
        # Hierarchie stattfindet, muss ein Teil-Dictionary die aktuelle Hierarchie abbilden. Auf diesem erfolgt das
        # Update.
        __startschluessel_dict: str = ""
        __startschluessel_dict = __aktuelles_speicherobjekt_baum.speicherdaten.schluessel
        __aktueller_schluessel_dict: str = ""
        __aktueller_speicherinhalt_dict: dict = {}
        __aktuelles_speicherobjekt_dict: dict = {}
        __laenge_letzter_pfad_dict: int = 0
        for __schluessel in __aktuelles_speicherobjekt_baum.speicherdaten.speicherinhalt.speicherelement.keys():
            __aktueller_speicherinhalt_dict[str(__schluessel)] = \
                __aktuelles_speicherobjekt_baum.speicherdaten.speicherinhalt.speicherelement[__schluessel]
        __aktuelles_speicherobjekt_dict[__aktuelles_speicherobjekt_baum.speicherdaten.schluessel] = \
            {"__speicherinhalt": __aktueller_speicherinhalt_dict}
        __dictionary_aus_baum.update(__aktuelles_speicherobjekt_dict)
        # initiales Befüllen des Dictionaries mit der obersten Ebene
        __aktueller_teil_dictionary = __dictionary_aus_baum
        __start_dictionary = __dictionary_aus_baum
        __speicherobjekte_in_queue = collections.deque()
        for __kinder in __aktuelles_speicherobjekt_baum.kinder:  # initiales Befüllen der Queue
            __speicherobjekte_in_queue.append(__kinder)
        while len(__speicherobjekte_in_queue) > 0:
            __aktuelles_speicherobjekt_queue = __speicherobjekte_in_queue.popleft()
            print("Aktuelles Speicherobjekt Queue", __aktuelles_speicherobjekt_queue.speicherdaten.schluessel, __aktuelles_speicherobjekt_queue.elternpfad)
            if len(__aktuelles_speicherobjekt_queue.elternpfad) < __laenge_letzter_pfad_dict:
                # Die Überprüfung ist nötig, um am Ende eines Pfades im Dictionary wieder in die richtige Hierarchie zu
                # springen. Dazu werden die Längen der entsprechenden Elternpfade verglichen. Besteht der neue
                # Elternpfad aus weniger Elementen als der letzte Elternpfad, wird das Dictionary von oben bis auf die
                # richtige Hierarchiestufe durchlaufen.
                __laenge_letzter_pfad_dict = len(__aktuelles_speicherobjekt_queue.elternpfad)
                __aktueller_teil_dictionary = __start_dictionary
                for __objekte in __aktuelles_speicherobjekt_queue.elternpfad:
                    __aktueller_teil_dictionary = __aktueller_teil_dictionary[__objekte]
            else:
                __aktueller_schluessel_dict = str(__aktuelles_speicherobjekt_queue.elternpfad[-1])
                print("Aktueller Schlüssel Dict", __aktueller_schluessel_dict)
                # Abgreifen des letzten Teil des Elternpfades. Umwandlung in einen String nötig , da sonst nicht immer
                # der Schlüssel richtig gelesen werden kann, z.B. bei Integer-Zahlen.
                __aktueller_teil_dictionary = __aktueller_teil_dictionary[__aktueller_schluessel_dict]
            __laenge_letzter_pfad_dict = len(__aktuelles_speicherobjekt_queue.elternpfad)
            __aktuelles_speicherobjekt_dict = {}
            # Speicherdaten muss wieder auf leer gesetzt werden, da es sonst um das neue Schlüssel-Wert-Paar ergänzt
            # wird, nicht das alte Schlüssel-Wert-Paar ersetzt wird.
            __aktueller_speicherinhalt_dict = {}
            for __schluessel in __aktuelles_speicherobjekt_queue.speicherdaten.speicherinhalt.speicherelement.keys():
                __aktueller_speicherinhalt_dict[str(__schluessel)] = \
                    __aktuelles_speicherobjekt_queue.speicherdaten.speicherinhalt.speicherelement[__schluessel]
            # Um zu vermeiden, dass es Verarbeitungsschwierigkeiten beim Umwandeln ins JSON-Format gibt, müssen die
            # Inhalte der Klasse Speicherinhalt aufgelöst und einzlen in ein Dictionary übertragen werden
            __aktuelles_speicherobjekt_dict[__aktuelles_speicherobjekt_queue.speicherdaten.schluessel] = \
                {"__speicherinhalt": __aktueller_speicherinhalt_dict}
            __aktueller_teil_dictionary.update(__aktuelles_speicherobjekt_dict)
            if len(__aktuelles_speicherobjekt_queue.kinder) > 0:  # Überprüfung, ob Kinder vorhanden sind
                __speicherobjekte_in_queue.extendleft(__aktuelles_speicherobjekt_queue.kinder)

        return __dictionary_aus_baum

    def zeige_datenspeicher_json(self):
        """
        Da der Inhalt eines Dictionaries in einer Zeile angezeigt wird, sind die einzelnen Hierarchien schwer zu
        erkennen. Mit der Methode erfolgt die Anzeige in Form eines JSON-Formats. Zur besseren Übersichtlichkeit
        werden die Schluessel-Wert-Paare alphabetisch sortiert.
        :return: None
        """
        __datenspeicher_als_dict: dict = {}
        __datenspeicher_als_dict = self.wandle_baum_in_dict()
        __datenspeicher_json = json.dumps(__datenspeicher_als_dict, sort_keys = True, indent = 4)
        print(__datenspeicher_json)


class Persistenz:

    def __init__(self, wurzel: str, datenspeicher: bool = False, speicherart: str = "Hauptspeicher"):
        self.__wurzel: str = wurzel
        self.__persistenz_datenspeicher: bool = datenspeicher  # steuert, ob die Daten im Datenspeicher abgelegt werden
        self.datenspeicher = Baum()
        self.datenspeicher.speicherdaten = Speicherdaten()
        self.datenspeicher.speicherdaten.schluessel = self.__wurzel
        self.speicherart: str = speicherart

    def zerlege_pfad(self, pfad: str) -> list:
        __pfad_ein: str = pfad
        __hierarchien: list = [""]
        if __pfad_ein[-1] == "/":
            __pfad = __pfad_ein.rstrip("/")
            # Um ein leeres Listenelement zu vermeiden, wird ein mögliches "/" auf der letzten Position gelöscht
        __hierarchien.extend(__pfad_ein.split("/"))
        for __elemente in __hierarchien:
            if __elemente == "":
                __hierarchien.remove("")

        return __hierarchien

    def erzeuge_schluessel_neueintrag(self, nummer: int) -> str:
        """

        :param nummer:
        :return:
        """
        __nummer_ein: int = nummer
        __schluessel: str = ""
        __schluessel = str(__nummer_ein) + "_" + str((random.randint(1, 1000) * random.randint(1, 1000)))

        return __schluessel

    def ermittele_letzten_eintrag_hierarchie(self, hierarchien: list) -> int:
        __hierarchien_ein: list = hierarchien
        __ressourcen: list = [0]
        for __eintrag in __hierarchien_ein:
            if not __eintrag.startswith("h_"):  # schließt Hierachien bei der Betrachtung aus
                __ressourcen.append(int(__eintrag))  # erfasse vorhandene Ressourcen in Hierachie

        return max(__ressourcen)

    def ersetze_letzen_schluessel(self, hierarchien: list) -> list:
        """
        Hierarchien sind in dem Dictionary mit dem Prefix "h_" gekennzeichnet. Der tatsächliche Speicher innerhalb der
        Hierarchie enthält kein solches Prexif. Um auf den Wert des angeforderten Speichers zugreifen zu können, muss
        das Prexif des letzten Schlüssels abgeschnitten werden.
        :param hierarchien: Liste der Hierarchien
        :return: Liste der Hierarchien mit dem geänderten letzten Schlüsselwort
        """
        __hierarchien_ein = hierarchien
        __hierarchien: list = []
        __hierarchien = __hierarchien_ein.copy()  # legt eine Kopie an, um Originalliste nicht zu verändern
        __letztes_schluesselwort = __hierarchien_ein[-1]
        __letztes_schluesselwort = __letztes_schluesselwort.rsplit("/", 1)[1]
        __hierarchien[-1] = __letztes_schluesselwort

        return __hierarchien

    def erzeuge_speicherobjekt(self, hierarchien: list, schluessel_neues_speicherobjekt: str):
        """
        Mit der Methode wird ein leeres Speicherdaten unter der richtigen Ressource angelegt, das später über die
        Methode aendere_speicherinhalt gefüllt wird.
        Grundlage: CRUD - Create
        :return: neu angelegtes Speicherdaten als leeres Dictionary
        """
        __hierarchien_ein: list = hierarchien
        print("Hierarchien ein", __hierarchien_ein)
        __schluessel_neues_speicherobjekt_ein = schluessel_neues_speicherobjekt
        print("Schlüssel neues Speicherobjekt", __schluessel_neues_speicherobjekt_ein, type(__schluessel_neues_speicherobjekt_ein))
        __neues_speicherobjekt = Baum()
        __neues_speicherobjekt.speicherdaten = Speicherdaten()
        __neues_speicherobjekt.speicherdaten.schluessel = __schluessel_neues_speicherobjekt_ein
        __neues_speicherobjekt.speicherdaten.speicherinhalt = Speicherinhalt()
        __neues_speicherobjekt.elternpfad.extend(__hierarchien_ein)
        __rueckgaben_daten_aus: dict = {"__speicherinhalt": None,
                                        "__rueckmeldung": "",
                                        "__erzeuge_speicherobjekt_erfolgreich": False,
                                        "__fehlercode": 0}
        __speicherobjekt_vorhanden: bool = True
        __aktuelles_speicherobjekt = self.datenspeicher
        __aktuelle_speicherobjekte: list = [__aktuelles_speicherobjekt]
        # Lädt die Wurzel in die Liste der Objekte, die in der nächsten Runde verarbeitet werden sollen
        for __schluessel in __hierarchien_ein:
            print("Schlüssel", __schluessel)
            if len(__aktuelle_speicherobjekte) == 0:
                __speicherobjekt_vorhanden = False
            else:
                for __speicherobjekt in __aktuelle_speicherobjekte:
                    print("Aktuelles Objekt", __speicherobjekt, __speicherobjekt.speicherdaten.schluessel)
                    if __schluessel == __speicherobjekt.speicherdaten.schluessel:
                        __aktuelles_speicherobjekt = __speicherobjekt
                        __aktuelle_speicherobjekte = __speicherobjekt.kinder
                        __speicherobjekt_vorhanden = True
                        break
                    else:
                        __speicherobjekt_vorhanden = False
        if __speicherobjekt_vorhanden:
            __aktuelles_speicherobjekt.kinder.append(__neues_speicherobjekt)
            print("Kinder", __aktuelles_speicherobjekt.kinder)
            __rueckgaben_daten_aus["__speicherinhalt"] = {}
            __rueckgaben_daten_aus["__rueckmeldung"] = "Neues Speicherobjekt konnte angelegt werden"
            __rueckgaben_daten_aus["__erzeuge_speicherobjekt_erfolgreich"] = True
            __rueckgaben_daten_aus["__fehlercode"] = 201
        else:
            __rueckgaben_daten_aus["__rueckmeldung"] = "Speicherobjekt kann nicht angelegt werden:" \
                                                       + " ... " \
                                                       + "/".join(__hierarchien_ein) \
                                                       + " fehlt."
            __rueckgaben_daten_aus["__fehlercode"] = 404
        print("Rückgabe erzeuge Speicherobjekt", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)


    def zeige_datenspeicher_json(self, uebergabedaten):
        """
        Da der Inhalt eines Dictionaries in einer Zeile angezeigt wird, sind die einzelnen Hierarchien schwer zu
        erkennen. Mit der Methode erfolgt die Anzeige in Form eines JSON-Formats. Zur besseren Übersichtlichkeit
        werden die Schluessel-Wert-Paare alphabetisch sortiert.
        :return: None
        """
        __uebergabedaten_ein = uebergabedaten
        __datenspeicher_json = json.dumps(__uebergabedaten_ein, sort_keys = True, indent = 4)
        print(__datenspeicher_json)

    def lese_speicherobjekt(self, hierarchien: list) -> json:
        # Ergänzung Parameter: Benutzer-ID, Passwort, Suchschlüssel)
        """

        Grundlage: CRUD - Read
        :return:
        """
        __hierarchien_ein = hierarchien
        __rueckgaben_daten_aus: dict = {"__speicherinhalt": None,
                                        "__rueckmeldung": "",
                                        "__lese_ressource_erfolgreich": False,
                                        "__fehlercode": 0}
        __speicherobjekt_vorhanden: bool = True
        __speicherinhalt_als_dict: dict = {}
        __aktuelles_speicherobjekt = self.datenspeicher
        __aktuelle_speicherobjekte: list = [__aktuelles_speicherobjekt]
        # Lädt die Wurzel in die Liste der Objekte, die in der nächsten Runde verarbeitet werden sollen
        for __schluessel in __hierarchien_ein:
            print("Schlüssel", __schluessel)
            if len(__aktuelle_speicherobjekte) == 0:
                __speicherobjekt_vorhanden = False
            else:
                for __speicherobjekt in __aktuelle_speicherobjekte:
                    print("Aktuelles Objekt", __speicherobjekt, __speicherobjekt.speicherdaten.schluessel)
                    if __schluessel == __speicherobjekt.speicherdaten.schluessel:
                        __aktuelles_speicherobjekt = __speicherobjekt
                        __aktuelle_speicherobjekte = __speicherobjekt.kinder
                        __letzter_schluessel = __speicherobjekt.speicherdaten.schluessel
                        __speicherobjekt_vorhanden = True
                        break
                    else:
                        __speicherobjekt_vorhanden = False
        if __speicherobjekt_vorhanden:
            for __schluessel in __aktuelles_speicherobjekt.speicherdaten.speicherinhalt.speicherelement:
                __speicherinhalt_als_dict[__schluessel] = \
                    __aktuelles_speicherobjekt.speicherdaten.speicherinhalt.speicherelement[__schluessel]
            __rueckgaben_daten_aus["__speicherinhalt"] = __speicherinhalt_als_dict
            __rueckgaben_daten_aus["__rueckmeldung"] = f"Ressource {'/'.join(__hierarchien_ein)} erfolgreich abgerufen"
            __rueckgaben_daten_aus["__lese_ressource_erfolgreich"] = True
            __rueckgaben_daten_aus["__fehlercode"] = 200
        else:
            __rueckgaben_daten_aus["__rueckmeldung"] = "Speicherobjekt nicht vorhanden"
            __rueckgaben_daten_aus["__fehlercode"] = 404
        print("Rückgabe lese Speicherobjekt", json.dumps(__rueckgaben_daten_aus))
        print(self.datenspeicher.wandle_baum_in_dict())

        return json.dumps(__rueckgaben_daten_aus)

    def aendere_speicherobjekt(self, hierarchien: list, inhalt_ein: dict):
        """

        Grundlage: CRUD - Update
        :return:
        """
        print("IN AENDERE_SPEICHEROBJEKT")
        __hierarchien_ein: list = hierarchien
        __inhalt_ein = inhalt_ein
        print("Hierarchien ein", __hierarchien_ein)
        print("Inhalt ein", __inhalt_ein)
        __rueckgaben_daten_aus: dict = {"__speicherinhalt": None,
                                        "__rueckmeldung": "",
                                        "__aendere_speicherobjekt_erfolgreich": False,
                                        "__fehlercode": 0}
        __speicherinhalt_als_dict: dict = {}
        __speicherobjekt_vorhanden: bool = True
        __letzter_schluessel: str = ""
        __aktuelles_speicherobjekt = self.datenspeicher
        __aktuelle_speicherobjekte: list = [__aktuelles_speicherobjekt]
        # Lädt die Wurzel in die Liste der Objekte, die in der nächsten Runde verarbeitet werden sollen
        for __schluessel in __hierarchien_ein:
            print("Schlüssel", __schluessel)
            if len(__aktuelle_speicherobjekte) == 0:
                __speicherobjekt_vorhanden = False
            else:
                for __speicherobjekt in __aktuelle_speicherobjekte:
                    print("Aktuelles Objekt", __speicherobjekt, __speicherobjekt.speicherdaten.schluessel)
                    if __schluessel == __speicherobjekt.speicherdaten.schluessel:
                        __aktuelles_speicherobjekt = __speicherobjekt
                        __aktuelle_speicherobjekte = __speicherobjekt.kinder
                        __letzter_schluessel = __speicherobjekt.speicherdaten.schluessel
                        print("Letzter Schlüssel", __letzter_schluessel, type(__schluessel))
                        __speicherobjekt_vorhanden = True
                        break
                    else:
                        __speicherobjekt_vorhanden = False
        if __speicherobjekt_vorhanden:
            __aktuelles_speicherobjekt.speicherdaten.speicherinhalt.speicherelement = __inhalt_ein[__letzter_schluessel]
            for __schluessel in __aktuelles_speicherobjekt.speicherdaten.speicherinhalt.speicherelement:
                __speicherinhalt_als_dict[__schluessel] = \
                    __aktuelles_speicherobjekt.speicherdaten.speicherinhalt.speicherelement[__schluessel]
            print("Speicherlement", __speicherinhalt_als_dict, type(__speicherinhalt_als_dict))
            # Umwandlung ist erforderlich, da JSON die Klasse Speicherinhalt nicht verarbeiten kann.
            # Kenzeichnung erfolgt durch Schlüssel "__speicherinhalt". Damit kann an anderer Stelle die Klasse
            # wiederhergestellt werden
            __rueckgaben_daten_aus["__speicherinhalt"] = __speicherinhalt_als_dict
            __rueckgaben_daten_aus["__rueckmeldung"] = "speicherobjekt geändert"
            __rueckgaben_daten_aus["__aendere_speicherobjekt_erfolgreich"] = True
            __rueckgaben_daten_aus["__fehlercode"] = 200
        else:
            __rueckgaben_daten_aus["__rueckmeldung"] = "speicherobjekt konnte nicht geändert werden, da nicht vorhanden"
            __rueckgaben_daten_aus["__fehlercode"] = 404

        print("Rückgabe aendere_speicherinhalt:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)

    def loesche_speicherobjekt(self, hierarchien: list):
        """
        
        Grundlage: CRUD - Delete
        :return:
        """
        print("IN LÖSCHE")
        __hierarchien_ein = hierarchien
        __rueckgaben_daten_aus: dict = {"__speicherinhalt": None,
                                        "__rueckmeldung": "",
                                        "__loesche_ressource_erfolgreich": False,
                                        "__fehlercode": 0}
        __speicherobjekt_vorhanden: bool = True
        __letzter_schluessel: str = ""
        __letzter_schluessel = __hierarchien_ein[-1]
        __aktuelles_speicherobjekt = self.datenspeicher
        __aktuelle_speicherobjekte: list = [__aktuelles_speicherobjekt]
        # Lädt die Wurzel in die Liste der Objekte, die in der nächsten Runde verarbeitet werden sollen
        for __schluessel in __hierarchien_ein:
            print("Schlüssel", __schluessel)
            if len(__aktuelle_speicherobjekte) == 0:
                __speicherobjekt_vorhanden = False
            else:
                for __speicherobjekt in __aktuelle_speicherobjekte:
                    print("Aktuelles Objekt", __speicherobjekt, __speicherobjekt.speicherdaten.schluessel)
                    if __schluessel == __speicherobjekt.speicherdaten.schluessel:
                        if __schluessel != __letzter_schluessel:
                            __aktuelles_speicherobjekt = __speicherobjekt
                            __aktuelle_speicherobjekte = __speicherobjekt.kinder
                        else:
                            print("Kinder vor", __aktuelles_speicherobjekt.kinder)
                            for __position, __kinder in enumerate(__aktuelles_speicherobjekt.kinder):
                                if __kinder.speicherdaten.schluessel == __letzter_schluessel:
                                    __aktuelles_speicherobjekt.kinder.pop(__position)
                            print("Kinder nach", __aktuelles_speicherobjekt.kinder)
                        __speicherobjekt_vorhanden = True
                        break
                    else:
                        __speicherobjekt_vorhanden = False
        if __speicherobjekt_vorhanden:
            __rueckgaben_daten_aus["__rueckmeldung"] = "Ressource gelöscht"
            __rueckgaben_daten_aus["__loesche_ressource_erfolgreich"] = True
            __rueckgaben_daten_aus["__fehlercode"] = 200
        else:
            __rueckgaben_daten_aus["__rueckmeldung"] = "Ressource nicht vorhanden"
            __rueckgaben_daten_aus["__fehlercode"] = 401
        print("Rückgabe loesche_speicherinhalt:", json.dumps(__rueckgaben_daten_aus))

        return json.dumps(__rueckgaben_daten_aus)
