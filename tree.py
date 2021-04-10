from collections import deque
import math


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class Tree:
    def balance_factor(self, root):
        return self.get_height(root.right) - self.get_height(root.left)

    def correct_height(self, root):
        height_left = self.get_height(root.left)
        height_right = self.get_height(root.right)
        root.height = (height_left + 1) if height_left > height_right else (height_right + 1)

    def rotate_right(self, root):
        q = root.left
        root.left = q.right
        q.right = root
        self.correct_height(root)
        self.correct_height(q)
        return q

    def rotate_left(self, root):
        p = root.right
        root.right = p.left
        p.left = root
        self.correct_height(root)
        self.correct_height(p)
        return p

    def balance(self, root):
        self.correct_height(root)
        if self.balance_factor(root) == 2:
            if self.balance_factor((root.right)) < 0:
                root.right = self.rotate_right((root.right))
            return self.rotate_left(root)
        if self.balance_factor(root) == -2:
            if self.balance_factor((root.left)) > 0:
                root.left = self.rotate_left((root.left))
            return self.rotate_right(root)
        return root

    def wide_order(self, root):
        q = deque()
        lst = []
        q.append(root)
        while len(q) > 0:
            n = q.popleft()
            if n:
                lst.append(n)
                q.append(n.left)
                q.append(n.right)
        return lst

    def display_order_wide(self, root):
        for i in self.wide_order(root):
            print(i.key, end=" ")

    def create_tree_of_array(self, arr, start, end):
        if end < start:
            return None
        mid = (start + end) // 2
        node = Node(arr[mid])
        node.left = self.create_tree_of_array(arr, start, mid - 1)
        node.right = self.create_tree_of_array(arr, mid + 1, end)
        return node

    def get_height(self, node):
        return node.height if node else 0

    def insert(self, node, key):
        if not node:
            return Node(key)
        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)
        return self.balance(node)

    def find(self, node, key):
        if not node:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self.find(node.left, key)
        else:
            return self.find(node.right, key)


def test_tree_of_array():
    arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    tree = Tree()
    root = tree.create_tree_of_array(arr, 0, len(arr) - 1)
    for i in tree.wide_order(root):
        assert i.height <= math.ceil(math.log2(len(arr)))
        if i.left:
            assert i.left.key < i.key
        if i.right:
            assert i.right.key > i.key


def test_insert_balance_tree():
    arr = [8, 3, 5, 9, 1]
    tree = Tree()
    root = Node(8)
    for i in range(1, len(arr)):
        root = tree.insert(root, arr[i])

    tree.display_order_wide(root)
    assert root.key == 5
    for i in tree.wide_order(root):
        assert i.height <= math.ceil(math.log2(5))
        if i.left:
            assert i.left.key < i.key
        if i.right:
            assert i.right.key > i.key
