"""
Diese Bibliothek enthält alle Klassen und Methoden zu AVL-Bäumen
"""

# from collections import deque


class AVLKnoten:

    def __init__(self, inhalt: object):
        """
        Mit der Methode wird ein Knoten aus Inhalt und den Zeigern nach links und rechts erzeugt.
        :param inhalt: Inhalt, der in dem Knoten hinterlegt werden soll. Der Datentyp soll flexibel sein.
        """
        self.inhalt: object = inhalt
        self.linkes_kind = None
        self.rechtes_kind = None

    def __str__(self):

        return str(self.inhalt)

    def __repr__(self):

        return str(self.inhalt)


class AVLBaum:
    """
    Es sollten noch folgende Methoden ergänzt werden:
    - einfügen_ohne_dublette
    - levelorder_traversierung
    - umgekehrte_inorder_traversierung
    - Suchfunktion
    """

    def __init__(self):
        """
        Mit dieser Methode wird ein AVL-Baum/AVL-Teilbaum erzeugt.
        """

        self.knoten = None
        self.hoehe = -1
        self.balance = 0

    def fuege_knoten_ein(self, inhalt: object):
        """
        Diese Methode fügt einen neuen Knoten an der richtigen Stelle im Baum ein.
        :param inhalt: Inhalt, der in dem Knoten hinterlegt werden soll. Der Datentyp soll flexibel sein.
        """
        __inhalt_ein: object = inhalt
        neuer_knoten = AVLKnoten(__inhalt_ein)
        if not self.knoten:
            self.knoten = neuer_knoten
            self.knoten.linkes_kind = AVLBaum()
            self.knoten.rechtes_kind = AVLBaum()
        elif __inhalt_ein < self.knoten.inhalt:
            self.knoten.linkes_kind.fuege_knoten_ein(__inhalt_ein)
        elif __inhalt_ein > self.knoten.inhalt:
            self.knoten.rechtes_kind.fuege_knoten_ein(__inhalt_ein)
        self.neu_balancieren()  # prüft, ob nach dem Einfügen ein Rebalancing nötig ist und führt dies durch

    def neu_balancieren(self):
        """
        Diese Methode balanciert den Baum nach Veränderungen durch Einfügen oder löschen neuer Knoten neu aus.
        """
        self.berechne_hoehe_neu(rekursiv = False)
        self.berechne_balance_neu(False)

        # Wenn der Balance-Faktor bei −1, 0, oder +1 ist keine Rotation nötig.
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:  # Der linke Teilbaum ist größer als der rechte Teilbaum
                if self.knoten.linkes_kind.balance < 0:
                    self.knoten.linkes_kind.rotiere_nach_links()
                    self.berechne_hoehe_neu()
                    self.berechne_balance_neu()
                self.rotiere_nach_rechts()
                self.berechne_hoehe_neu()
                self.berechne_balance_neu()

            if self.balance < -1:  # Der rechte Teilbaum ist größer als der linke Teilbaum
                if self.knoten.rechtes_kind.balance > 0:
                    self.knoten.rechtes_kind.rotiere_nach_rechts()  # we're in case III
                    self.berechne_hoehe_neu()
                    self.berechne_balance_neu()
                self.rotiere_nach_links()
                self.berechne_hoehe_neu()
                self.berechne_balance_neu()

    def berechne_hoehe_neu(self, rekursiv = True):
        """
        Diese Methode berechnet die aktuelle Höhe des Teil(Baumes). Diese Höhe ergibt sich aus dem Maximum des linken
        und rechten Teilbaums +1 für die Wurzel.
        :param rekursiv:
        """
        __rekursiv_ein = rekursiv
        if self.knoten:
            if __rekursiv_ein:
                if self.knoten.linkes_kind:
                    self.knoten.linkes_kind.berechne_hoehe_neu()
                if self.knoten.rechtes_kind:
                    self.knoten.rechtes_kind.berechne_hoehe_neu()
            self.hoehe = 1 + max(self.knoten.linkes_kind.hoehe, self.knoten.rechtes_kind.hoehe)
        else:
            self.hoehe = -1

    def berechne_balance_neu(self, rekursiv = True):
        """
        Diese Methode berechnet den aktuellen Balance-Faktor des (Teil)Baums. Die Formel für den Balance-Faktor lautet:
        Balance = Höhe des linken Teilbaums - Höhe des rechten Teilbaums
        :param rekursiv:
        """
        __rekursiv_ein = rekursiv
        if self.knoten:
            if __rekursiv_ein:
                if self.knoten.linkes_kind:
                    self.knoten.linkes_kind.berechne_balance_neu()
                if self.knoten.rechtes_kind:
                    self.knoten.rechtes_kind.berechne_balance_neu()
            self.balance = self.knoten.linkes_kind.hoehe - self.knoten.rechtes_kind.hoehe
        else:
            self.balance = 0

    def rotiere_nach_rechts(self):
        """
        Diese Methode führt eine Rotation des (Teil)Baums nach rechts aus.
        """
        __neue_wurzel = self.knoten.linkes_kind.knoten
        __neues_linkes_kind = __neue_wurzel.rechtes_kind.knoten
        __alte_wurzel = self.knoten
        self.knoten = __neue_wurzel
        __alte_wurzel.linkes_kind.knoten = __neues_linkes_kind
        __neue_wurzel.rechtes_kind.knoten = __alte_wurzel

    def rotiere_nach_links(self):
        """
        Diese Methode führt eine Rotation des (Teil)Baums nach links aus.
        """
        __neue_wurzel = self.knoten.rechtes_kind.knoten
        __neues_linkes_kind = __neue_wurzel.linkes_kind.knoten
        __alte_wurzel = self.knoten
        self.knoten = __neue_wurzel
        __alte_wurzel.rechtes_kind.knoten = __neues_linkes_kind
        __neue_wurzel.linkes_kind.knoten = __alte_wurzel

    def loesche_knoten(self, inhalt: object):
        """
        Diese Methode löscht einen Knoten aus einem (Teil)Baum.
        :param inhalt:
        """
        __inhalt_ein: object = inhalt
        if self.knoten is not None:
            if self.knoten.inhalt == __inhalt_ein:
                if not self.knoten.linkes_kind.knoten and not self.knoten.rechtes_kind.knoten:
                    self.knoten = None
                    # Der Knoten wird nur direkt gelöscht, wenn keine Kinder vorhanden sind
                elif not self.knoten.linkes_kind.knoten:
                    self.knoten = self.knoten.rechtes_kind.knoten
                    # Falls der Knoten nur ein rechtes Kind hat, ersetzt dieses die Wurzel
                elif not self.knoten.rechtes_kind.knoten:
                    self.knoten = self.knoten.linkes_kind.knoten
                    # Falls der Knoten nur ein linkes Kind hat, ersetzt dieses die Wurzel
                else:
                    __nachfolger = self.knoten.rechtes_kind.knoten
                    # Suche den kleinten Knoten im rechten Teilbaum als Nachfolger oder
                    # den größten Knoten im linken Teilbaum als Vorgängen
                    while __nachfolger and __nachfolger.linkes_kind.knoten:
                        __nachfolger = __nachfolger.linkes_kind.knoten
                    if __nachfolger:
                        self.knoten.inhalt = __nachfolger.inhalt
                        self.knoten.rechtes_kind.loesche_knoten(__nachfolger.inhalt)
                        # Lösche den Nachfolger vom rechten Teilbaum
            elif __inhalt_ein < self.knoten.inhalt:
                self.knoten.linkes_kind.loesche_knoten(__inhalt_ein)
            elif __inhalt_ein > self.knoten.inhalt:
                self.knoten.rechtes_kind.loesche_knoten(__inhalt_ein)
            self.neu_balancieren()  # Balanciere den (Teil)Baum neu aus.

    def inorder_traversieren(self):
        """
        Diese Methode durchläuft den (Teil)Baum in der Reihenfolge
        1. linker Teilbaum
        2. Wurzel
        3. rechter Teilbaum
        :return __ergebnis: Liste aller Inhalte in der aufgenommenen Reihenfolge
        """
        __ergebnis: list = []
        if not self.knoten:
            return __ergebnis
        __ergebnis.extend(self.knoten.linkes_kind.inorder_traversieren())
        __ergebnis.append(self.knoten.inhalt)
        __ergebnis.extend(self.knoten.rechtes_kind.inorder_traversieren())

        return __ergebnis

    def preorder_traversieren(self):
        """
        Diese Methode durchläuft den (Teil)Baum in der Reihenfolge
        1. Wurzel
        2. linker Teilbaum
        3. rechter Teilbaum
        :return __ergebnis: Liste aller Inhalte in der aufgenommenen Reihenfolge
        """
        __ergebnis: list = []
        if not self.knoten:
            return __ergebnis
        __ergebnis.append(self.knoten.inhalt)
        __ergebnis.extend(self.knoten.linkes_kind.inorder_traversieren())
        __ergebnis.extend(self.knoten.rechtes_kind.inorder_traversieren())

        return __ergebnis

    def postorder_traversieren(self):
        """
        Diese Methode durchläuft den (Teil)Baum in der Reihenfolge
        1. linker Teilbaum
        2. rechter Teilbaum
        3. Wurzel
        :return __ergebnis: Liste aller Inhalte in der aufgenommenen Reihenfolge
        """
        __ergebnis: list = []
        if not self.knoten:
            return __ergebnis
        __ergebnis.extend(self.knoten.linkes_kind.inorder_traversieren())
        __ergebnis.extend(self.knoten.rechtes_kind.inorder_traversieren())
        __ergebnis.append(self.knoten.inhalt)

        return __ergebnis

    def anzeigen(self, knoten = None, level = 0):
        """
        Diese Methode zeigt den (Teil)Baum an.
        :param knoten:
        :param level:
        """
        __knoten_ein = knoten
        __level_ein = level
        if not __knoten_ein:
            __knoten_ein = self.knoten
        if __knoten_ein.rechtes_kind.knoten:
            self.anzeigen(__knoten_ein.rechtes_kind.knoten, __level_ein + 1)
            print(('\t' * __level_ein), '    /')
        print(('\t' * level), __knoten_ein)
        if __knoten_ein.linkes_kind.knoten:
            print(('\t' * __level_ein), '    \\')
            self.anzeigen(__knoten_ein.linkes_kind.knoten, __level_ein + 1)


# Demo
if __name__ == '__main__':
    baum = AVLBaum()
    data_starwars = ['Luke', 'Leia', 'Han', 'Obi Wan', 'Chewbacca', 'Darth Vader', 'Yoda', 'Rey', 'Finn', 'Boba Fett']
    #    data_numbers = [6, 3, 9, 2, 5, 8, 10, 1, 4, 7, 11]

    for elemente in data_starwars:
        baum.fuege_knoten_ein(elemente)

    #   for schluessel in [4,3]:
    #        tree.delete(schluessel)

    print(baum.inorder_traversieren())
    print(baum.preorder_traversieren())
    print(baum.postorder_traversieren())
    #    print(Tree.search(1))
    baum.anzeigen()
