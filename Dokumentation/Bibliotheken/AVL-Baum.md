"""
Diese Bibliothek enthält alle Klassen und Methoden zu AVL-Bäumen
"""

from collections import deque


class AVLNode(object):
    '''
    A Node in an AVL Tree.
    '''

    def __init__(self, key):
        '''
        Constructor for an AVL Node, including content and pointers to left and right side.
        :param Key: Content for the node
        '''

        # The Node's Key
        self.key = key
        # The Node's Left child
        self.left = None
        # The Node's Right child
        self.right = None

    def __str__(self):
        '''
        String representation.
        :return: Content of the node
        '''

        return str(self.key)

    def __repr__(self):
        '''
        String representation.
        :return: Content of the node
        '''

        return str(self.key)


class AVLTree(object):
    '''
    An AVL Tree.
    '''

    def __init__(self):
        '''
        Constructor for an AVL Tree.
        '''

        # Root Node of the Tree.
        self.node = None
        # Height of the Tree.
        self.height = -1
        # Balance factor of the Tree.
        self.balance = 0

    def insert(self, key):
        '''
        Inserts a new key in the node.
        :param key: Content of node.
        :return: None
        '''

        # Create new Node
        new_node = AVLNode(key)

        # Initial Tree
        if not self.node:
            self.node = new_node
            self.node.left = AVLTree()
            self.node.right = AVLTree()
        # Insert Key to the Left subtree
        elif key < self.node.key:
            self.node.left.insert(key)
        # Insert Key to the Right subtree
        elif key > self.node.key:
            self.node.right.insert(key)

        # Rebalance the AVL Tree if needed
        self.rebalance()

    def rebalance(self):
        '''
        Rebalances an AVL-Tree. After inserting or deleting a Node,
        it is necessary to check each of the Node's ancestors for consistency with the rules of AVL
        :return: None
        '''

        # Check if we need to rebalance the Tree
        #   update Height
        #   Balance Tree
        self.update_heights(recursive=False)
        self.update_balances(False)

        # For each Node checked,
        #   if the Balance factor remains −1, 0, or +1 then no rotations are necessary.
        while self.balance < -1 or self.balance > 1:
            # Left subtree is larger than Right subtree
            if self.balance > 1:

                # Left Right Case -> rotate y,z to the Left
                if self.node.left.balance < 0:
                    #     x               x
                    #    / \             / \
                    #   y   D           z   D
                    #  / \        ->   / \
                    # A   z           y   C
                    #    / \         / \
                    #   B   C       A   B
                    self.node.left.rotate_left()
                    self.update_heights()
                    self.update_balances()

                # Left Left Case -> rotate z,x to the Right
                #       x                 z
                #      / \              /   \
                #     z   D            y     x
                #    / \         ->   / \   / \
                #   y   C            A   B C   D
                #  / \
                # A   B
                self.rotate_right()
                self.update_heights()
                self.update_balances()

            # Right subtree is larger than Left subtree
            if self.balance < -1:

                # Right Left Case -> rotate x,z to the Right
                if self.node.right.balance > 0:
                    #     y               y
                    #    / \             / \
                    #   A   x           A   z
                    #      / \    ->       / \
                    #     z   D           B   x
                    #    / \                 / \
                    #   B   C               C   D
                    self.node.right.rotate_right()  # we're in case III
                    self.update_heights()
                    self.update_balances()

                # Right Right Case -> rotate y,x to the Left
                #       y                 z
                #      / \              /   \
                #     A   z            y     x
                #        / \     ->   / \   / \
                #       B   x        A   B C   D
                #          / \
                #         C   D
                self.rotate_left()
                self.update_heights()
                self.update_balances()

    def update_heights(self, recursive=True):
        '''
        Update Tree Height

        Tree Height is max Height of either Left or Right subtrees +1 for root of the Tree
        '''
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.update_heights()
                if self.node.right:
                    self.node.right.update_heights()

            self.height = 1 + max(self.node.left.height, self.node.right.height)
        else:
            self.height = -1

    def update_balances(self, Recursive=True):
        '''
        Calculate Tree Balance factor

        The Balance factor is calculated as follows:
            Balance = Height(Left subtree) - Height(Right subtree).
        '''
        if self.node:
            if Recursive:
                if self.node.left:
                    self.node.left.update_balances()
                if self.node.right:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
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
        if self.node != None:
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
            print(('\t' * level), ('    /'))

        print(('\t' * level), node)

        if node.left.node:
            print(('\t' * level), ('    \\'))
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
    tree = AVLTree()
    data_starwars = ['Luke', 'Leia', 'Han', 'Obi Wan', 'Chewbacca', 'Darth Vader', 'Yoda', 'Rey', 'Finn', 'Boba Fett']
    #    data_numbers = [6, 3, 9, 2, 5, 8, 10, 1, 4, 7, 11]

    for key in data_starwars:
        tree.insert(key)

    #   for key in [4,3]:
    #        tree.delete(key)

    print(tree.inorder_traverse())
    print(tree.preorder_traverse())
    print(tree.postorder_traverse())
    #    print(Tree.search(1))
    tree.display()