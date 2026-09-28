"""
Self-Balancing AVL Tree with Rotation Tracking (DSA Topic)
Demonstrates tree balance, O(log n) lookups, and recorded Left/Right rotations.
"""
from typing import Optional, List, Dict, Any

class AVLNode:
    def __init__(self, key: int, payload: Any = None):
        self.key = key
        self.payload = payload
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height: int = 1


class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.rotation_log: List[Dict[str, Any]] = []

    def get_height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def get_balance(self, node: Optional[AVLNode]) -> int:
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        self.rotation_log.append({"type": "RIGHT_ROTATION (RR)", "pivot": y.key, "new_root": x.key})
        return x

    def left_rotate(self, x: AVLNode) -> AVLNode:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        self.rotation_log.append({"type": "LEFT_ROTATION (LL)", "pivot": x.key, "new_root": y.key})
        return y

    def insert(self, key: int, payload: Any = None) -> None:
        self.root = self._insert_node(self.root, key, payload)

    def _insert_node(self, node: Optional[AVLNode], key: int, payload: Any) -> AVLNode:
        if not node:
            return AVLNode(key, payload)

        if key < node.key:
            node.left = self._insert_node(node.left, key, payload)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, payload)
        else:
            return node # duplicate keys ignored

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        # Right Right
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        # Left Right
        if balance > 1 and key > node.left.key:
            self.rotation_log.append({"type": "LEFT_RIGHT_COMPOUND (LR)", "pivot": node.key})
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Left
        if balance < -1 and key < node.right.key:
            self.rotation_log.append({"type": "RIGHT_LEFT_COMPOUND (RL)", "pivot": node.key})
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def inorder_traversal(self) -> List[int]:
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res
