class BSTNode:
    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None


def bst_insert(root, key: int):
    if root is None:
        return BSTNode(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    elif key > root.key:
        root.right = bst_insert(root.right, key)
    return root


def bst_min(node):
    while node.left is not None:
        node = node.left
    return node


def bst_delete(root, key: int):
    if root is None:
        return None
    if key < root.key:
        root.left = bst_delete(root.left, key)
    elif key > root.key:
        root.right = bst_delete(root.right, key)
    else:
        if root.left is not None and root.right is not None:
            succ = bst_min(root.right)
            root.key = succ.key
            root.right = bst_delete(root.right, succ.key)
        elif root.left is not None:
            return root.left
        elif root.right is not None:
            return root.right
        else:
            return None
    return root


def bst_height(node) -> int:
    if node is None:
        return 0
    return 1 + max(bst_height(node.left), bst_height(node.right))


class RBNode:
    def __init__(self, key=None, color: str = "BLACK"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RBTree:

    def __init__(self):
        self.NIL = RBNode(key=None, color="BLACK")
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key: int):
        z = RBNode(key=key, color="RED")
        z.left = self.NIL
        z.right = self.NIL
        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            x = x.left if z.key < x.key else x.right
        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        while z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right
                if uncle.color == "RED":
                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)
            else:
                uncle = z.parent.parent.left
                if uncle.color == "RED":
                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.left_rotate(z.parent.parent)
        self.root.color = "BLACK"

    def search(self, key: int):
        x = self.root
        while x != self.NIL and x.key != key:
            x = x.left if key < x.key else x.right
        return x

    def minimum(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, key: int):
        z = self.search(key)
        if z == self.NIL:
            return
        y = z
        y_orig_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_orig_color == "BLACK":
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"

    def height(self, node=None) -> int:
        if node is None:
            node = self.root
        if node == self.NIL:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def verify(self) -> int:
        """Перевіряє властивості ЧЧД та повертає чорну висоту (без NIL-листів)."""
        assert self.root.color == "BLACK", "Корінь повинен бути чорним!"

        def _check(node) -> int:
            if node == self.NIL:
                return 0
            if node.color == "RED":
                assert node.left.color == "BLACK" and node.right.color == "BLACK"
            lh = _check(node.left)
            rh = _check(node.right)
            assert lh == rh, f"Порушення чорної висоти у вузлі {node.key}"
            return lh + (1 if node.color == "BLACK" else 0)

        return _check(self.root)


def get_traversals_and_stack(root, is_rb: bool = False):
    inorder, preorder, postorder, stack_trace, cur = [], [], [], [], []

    def is_nil(node):
        return node is None or (is_rb and node.key is None)

    def _in(node):
        if is_nil(node):
            return
        cur.append(node.key)
        stack_trace.append(list(cur))
        if not is_nil(node.left):
            _in(node.left)
            stack_trace.append(list(cur))
        inorder.append(node.key)
        if not is_nil(node.right):
            _in(node.right)
            stack_trace.append(list(cur))
        cur.pop()

    def _pre(node):
        if is_nil(node):
            return
        preorder.append(node.key)
        _pre(node.left)
        _pre(node.right)

    def _post(node):
        if is_nil(node):
            return
        _post(node.left)
        _post(node.right)
        postorder.append(node.key)

    _in(root)
    _pre(root)
    _post(root)
    return inorder, preorder, postorder, stack_trace


if __name__ == "__main__":
    # Варіант № 15
    SEQ = [19, 75, 43, 31, 5, 66, 62, 34, 76]

    bst = None
    rb = RBTree()
    for val in SEQ:
        bst = bst_insert(bst, val)
        rb.insert(val)

    bh = rb.verify()
    print(f"Варіант № 15: {SEQ}")
    print(f"Висота BST: {bst_height(bst)}")
    print(f"Висота ЧЧД: {rb.height()}, чорна висота ЧЧД: {bh}")

    bst_in, bst_pre, bst_post, bst_st = get_traversals_and_stack(bst, is_rb=False)
    rb_in, rb_pre, rb_post, rb_st = get_traversals_and_stack(rb.root, is_rb=True)

    print("\n=== Обходи BST ===")
    print("Inorder:  ", bst_in)
    print("Preorder: ", bst_pre)
    print("Postorder:", bst_post)
    print("Макс. глибина стека BST:", max(len(s) for s in bst_st))

    print("\n=== Обходи ЧЧД ===")
    print("Inorder:  ", rb_in)
    print("Preorder: ", rb_pre)
    print("Postorder:", rb_post)
    print("Макс. глибина стека ЧЧД:", max(len(s) for s in rb_st))

    for key in (75, 5, 19):
        bst = bst_delete(bst, key)
    print("\nBST після видалення 75, 5, 19 (inorder):", get_traversals_and_stack(bst)[0])

    for key in (5, 19, 43):
        rb.delete(key)
        bh_after = rb.verify()
        print(f"ЧЧД після видалення {key}: OK (корінь={rb.root.key}, чорна висота={bh_after})")
