"""
Diese Bibliothek enthält alle Klassen und Methoden zu AVL-Bäumen
"""

from collections import deque


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

    def rotate_right(self):
        '''
        Right rotation
            set self as the Right subtree of Left subree
        '''
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def rotate_left(self):
        '''
        Left rotation
            set self as the Left subtree of Right subree
        '''
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def delete(self, key):
        '''
        Delete Key from the Tree

        Let Node X be the Node with the value we need to delete,
        and let Node Y be a Node in the Tree we need to find to take Node X's place,
        and let Node Z be the actual Node we take out of the Tree.

        Steps to consider when deleting a Node in an AVL Tree are the following:

            * If Node X is a leaf or has only one child, skip to step 5. (Node Z will be Node X)
                * Otherwise, determine Node Y by finding the largest Node in Node X's Left sub Tree
                    (in-order predecessor) or the smallest in its Right sub Tree (in-order Successor).
                * Replace Node X with Node Y (remember, Tree structure doesn't change here, only the values).
                    In this step, Node X is essentially deleted when its internal values were overwritten with Node Y's.
                * Choose Node Z to be the old Node Y.
            * Attach Node Z's subtree to its parent (if it has a subtree). If Node Z's parent is null,
                update root. (Node Z is currently root)
            * Delete Node Z.
            * Retrace the path back up the Tree (starting with Node Z's parent) to the root,
                adjusting the Balance factors as needed.
        '''
        if self.node is not None:
            if self.node.key == key:
                # Key found in leaf Node, just erase it
                if not self.node.left.node and not self.node.right.node:
                    self.node = None
                # Node has only one subtree (Right), replace root with that one
                elif not self.node.left.node:
                    self.node = self.node.right.node
                # Node has only one subtree (Left), replace root with that one
                elif not self.node.right.node:
                    self.node = self.node.left.node
                else:
                    # Find  Successor as smallest Node in Right subtree or
                    #       predecessor as largest Node in Left subtree
                    successor = self.node.right.node
                    while successor and successor.left.node:
                        successor = successor.left.node

                    if successor:
                        self.node.key = successor.key

                        # Delete Successor from the replaced Node Right subree
                        self.node.right.delete(successor.key)

            elif key < self.node.key:
                self.node.left.delete(key)

            elif key > self.node.key:
                self.node.right.delete(key)

            # ReBalance Tree
            self.rebalance()

    def inorder_traverse(self):
        '''
        Inorder traversal of the Tree
            Left subree + root + Right subtree
        '''
        result = []

        if not self.node:
            return result

        result.extend(self.node.left.inorder_traverse())
        result.append(self.node.key)
        result.extend(self.node.right.inorder_traverse())

        return result

    def preorder_traverse(self):
        '''
        Inorder traversal of the Tree
            root + Left subree + Right subtree
        '''
        result = []

        if not self.node:
            return result

        result.append(self.node.key)
        result.extend(self.node.left.inorder_traverse())
        result.extend(self.node.right.inorder_traverse())

        return result

    def postorder_traverse(self):
        '''
        Inorder traversal of the Tree
            Left subree + Right subtree + root
        '''
        result = []

        if not self.node:
            return result

        result.extend(self.node.left.inorder_traverse())
        result.extend(self.node.right.inorder_traverse())
        result.append(self.node.key)

        return result

    #
    #    def search(self, Searchkey):
    #        '''
    #        Search for Searchkey in tree
    #       '''
    #
    #       if type (Searchkey) == str:
    #           Searchkey = Searchkey.lower()
    #           Temp = self.Node.Key.lower()
    #       if self.Node:
    #           if Temp == Searchkey:
    #               return True
    #           elif Searchkey < Temp:
    #               return self.Node.Left.search(Searchkey)
    #           elif Searchkey > Temp:
    #               return self.Node.Right.search(Searchkey)
    #           else:
    #               return False
    # '''

    def display(self, node=None, level=0):
        if not node:
            node = self.node

        if node.right.node:
            self.display(node.right.node, level + 1)
            print(('\t' * level), '    /')

        print(('\t' * level), node)

        if node.left.node:
            print(('\t' * level), '    \\')
            self.display(node.left.node, level + 1)


'''
ToDo:
- insert_without_double
- levelorder_traverse
- reverse_inorder_traverse
- search
'''

# Demo
if __name__ == '__main__':
    baum = AVLBaum()
    data_starwars = ['Luke', 'Leia', 'Han', 'Obi Wan', 'Chewbacca', 'Darth Vader', 'Yoda', 'Rey', 'Finn', 'Boba Fett']
    #    data_numbers = [6, 3, 9, 2, 5, 8, 10, 1, 4, 7, 11]

    for inhalt in data_starwars:
        baum.insert(inhalt)

    #   for schluessel in [4,3]:
    #        tree.delete(schluessel)

    print(baum.inorder_traverse())
    print(baum.preorder_traverse())
    print(baum.postorder_traverse())
    #    print(Tree.search(1))
    baum.display()
