import collections

class Speicherinhalt:

    def __init__(self):
        self.speicherdaten: dict = {}


class Speicherelement:

    def __init__(self, schluessel: str = ""):
        self.schluessel_ein = schluessel
        self.speicherinhalt = Speicherinhalt()


class Baum:

    def __init__(self):
        self.speicherelement = None
        self.kinder: list = []
        self.elternpfad: list = []

    def wandle_baum_in_dict(self) -> dict:
        """
        Diese Methode wandelt die Baumstruktur der Persistenz in ein Dictionary um, damit dieses später im JSON-Format
        übertragen werden kann. Dazu werden der Reihe nach alle Speicherobjekte im Baum durchgegangen und in eine 
        Queue geschrieben, bis das letzte Objekt eines Pfads erreicht ist (die Variable kinder enthält eine leere 
        Liste). Der Vorteil der Speicherung von Objekten in der Queue besteht darin, dass sobald das Pfadende erreicht
        ist, der Baum nicht wieder von oben durchlaufen werden muss - anders als beim Dictionary. Die Methode endet,
        wenn kein Objekt mehr in der Queue liegt, d.h. alle Objekte abgearbeitet wurden. Es müssen zwei Pfade gesteuert
        werden: der Pfad durch den Baum und der Pfad durch das Dictionary.
        :return: den umgewandelten Baum als dict
        """
        __aktuelle_hierarchie_in_baum = datenspeicher
        __dictionary_aus_baum: dict = {}
        __aktueller_teil_dictionary: dict = {}  
        # Damit beim Update des Dictionaries die Ergänzung um das aktuelle Speicherelement nur auf der entsprechenden
        # Hierarchie stattfindet, muss ein Teil-Dictionary die aktuelle Hierarchie abbilden. Auf diesem erfolgt das
        # Update.
        __starthierarchie_in_dict: str = ""
        __starthierarchie_in_dict = __aktuelle_hierarchie_in_baum.speicherelement.schluessel_ein
        __dictionary_aus_baum[__starthierarchie_in_dict] = {}
        __aktuelle_hierarchie_in_dict: str = ""
        __aktuelles_speicherelement = Speicherinhalt()
        __laenge_letzter_pfad: int = 0
        __aktuelles_speicherelement.speicherdaten = \
            __aktuelle_hierarchie_in_baum.speicherelement.speicherinhalt.speicherdaten
        print("Aktuelles Speicherelement", __aktuelles_speicherelement, type(__aktuelles_speicherelement))
        __dictionary_aus_baum[__starthierarchie_in_dict] = __aktuelles_speicherelement.speicherdaten
        print("Dict aus Baum", __dictionary_aus_baum, type(__dictionary_aus_baum["prints"]))
        # initiales Befüllen des Dictionaries mit der obersten Ebene
        __aktueller_teil_dictionary = __dictionary_aus_baum
        __start_dictionary = __dictionary_aus_baum
        __speicherelemente_in_queue = collections.deque()
        for __kinder in __aktuelle_hierarchie_in_baum.kinder:  # initiales Befüllen der Queue
            __speicherelemente_in_queue.append(__kinder)
        while len(__speicherelemente_in_queue) > 0:
            __aktuelles_element_aus_queue = __speicherelemente_in_queue.popleft()
            if len(__aktuelles_element_aus_queue.elternpfad) < __laenge_letzter_pfad:
            # Die Überprüfung ist nötig, um am Ende eines Pfades im Dictionary wieder in die richtige Hierarchie zu
            # springen. Dazu werden die Längen der entsprechenden Elternpfade verglichen. Besteht der neue Elternpfad
            # weniger Elementen als der letzte Elternpfad, wird das Dictionary von oben bis auf die richtige
            # Hierarchiestufe durchlaufen.
                __laenge_letzter_pfad = len(__aktuelles_element_aus_queue.elternpfad)
                __aktueller_teil_dictionary = __start_dictionary
                for __elemente in __aktuelles_element_aus_queue.elternpfad:
                    __aktueller_teil_dictionary = __aktueller_teil_dictionary[__elemente]
            else:
                __aktuelle_hierarchie_in_dict = str(__aktuelles_element_aus_queue.elternpfad[-1])
                # Abgreifen des letzten Teil des Elternpfades. Umwandlung in einen String nötig , da sonst nicht immer
                # der Schlüssel richtig gelesen werden kann, z.B. bei Integer-Zahlen.
                __aktueller_teil_dictionary = __aktueller_teil_dictionary[__aktuelle_hierarchie_in_dict]
                print("Typ __aktueller_teil_dictionary", __aktueller_teil_dictionary, type(__aktueller_teil_dictionary))
            __laenge_letzter_pfad = len(__aktuelles_element_aus_queue.elternpfad)
            __aktuelles_speicherelement.speicherdaten = {}
            # Speicherelement muss wieder auf leer gesetzt werden, da es sonst um das neue Schlüssel-Wert-Paar ergänzt
            # wird, nicht das alte Schlüssel-Wert-Paar ersetzt wird.
            __aktuelles_speicherelement.speicherdaten[__aktuelles_element_aus_queue.speicherelement.schluessel_ein] = \
                __aktuelles_element_aus_queue.speicherelement.speicherinhalt.speicherdaten
            __aktueller_teil_dictionary.update(__aktuelles_speicherelement)
            print("Dictionary",__dictionary_aus_baum)
            if __aktuelles_element_aus_queue.kinder != []:
                __speicherelemente_in_queue.extendleft(__aktuelles_element_aus_queue.kinder)

        return __dictionary_aus_baum

    def wandle_dict_in_baum(self):
        __baum_aus_dictionary = Baum()

        return __baum_aus_dictionary



datenspeicher = Baum()

wurzel = Speicherelement("prints")
wurzel.speicherinhalt.speicherdaten["0"] = "test"

datenspeicher.speicherelement = wurzel

aktuelle_hierarchie = datenspeicher

print("Aktuelle Hierarchie", aktuelle_hierarchie.kinder)

# hinzufügen

neues_speicherelement = Speicherelement("1000_4711")
neues_speicherelement.speicherinhalt.speicherdaten["1"] = "Test 1"
neue_ressource = Baum()
neue_ressource.elternpfad = ["prints"]
neue_ressource.speicherelement = neues_speicherelement
aktuelle_hierarchie.kinder.append(neue_ressource)

aktuelle_hierarchie = aktuelle_hierarchie.kinder[0]
print("Aktuelle Hierarchie", aktuelle_hierarchie.speicherelement.schluessel_ein)

neues_speicherelement = Speicherelement("3000_0815")
neues_speicherelement.speicherinhalt.speicherdaten["3"] = "Test 3"
neue_ressource = Baum()
neue_ressource.elternpfad = ["prints", "1000_4711"]
neue_ressource.speicherelement = neues_speicherelement
aktuelle_hierarchie.kinder.append(neue_ressource)
print("Aktuelle Hierarchie Kinder", aktuelle_hierarchie.kinder[0].speicherelement.schluessel_ein)
print("Aktuelle Hierarchie Elternpfad", aktuelle_hierarchie.kinder[0].elternpfad)

aktuelle_hierarchie = datenspeicher

neues_speicherelement = Speicherelement("2000_0815")
neues_speicherelement.speicherinhalt.speicherdaten["2"] = "Test 2"
neue_ressource = Baum()
neue_ressource.elternpfad = ["prints"]
neue_ressource.speicherelement = neues_speicherelement
aktuelle_hierarchie.kinder.append(neue_ressource)

print("Aktuelle Hierarchie Kinder", aktuelle_hierarchie.kinder)

aktuelle_hierarchie = aktuelle_hierarchie.kinder[1]
print(aktuelle_hierarchie)
print(aktuelle_hierarchie.speicherelement.schluessel_ein)


print("Aktuelle Hierarchie", aktuelle_hierarchie.speicherelement.schluessel_ein)

for kinder in datenspeicher.kinder:
    print("Schlüssel", kinder.speicherelement.schluessel_ein)
    print("Speicherinhalt", kinder.speicherelement.speicherinhalt.speicherdaten)
    print("Eltern", kinder.elternpfad)

print("--------------------------------------------")

"""
# löschen

aktuelle_hierarchie = datenspeicher

for nummer, kinder in enumerate(aktuelle_hierarchie.kinder):
    if str(kinder.speicherelement.schluessel_ein) == "2000_0815":
        nummer_loesch_ressource = nummer
del datenspeicher.kinder[nummer_loesch_ressource]

for kinder in aktuelle_hierarchie.kinder:
    print("Schlüssel", kinder.speicherelement.schluessel_ein)
    print("Speicherinhalt", kinder.speicherelement.speicherinhalt.speicherdaten)
    print("Eltern", kinder.eltern)

"""

datenspeicher.wandle_baum_in_dict()