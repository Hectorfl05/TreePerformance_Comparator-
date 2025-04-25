from node import Node

class BStarNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []  # Lista de claves (instancias de Node) almacenadas en el nodo
        self.children = []  # Lista de hijos del nodo
        self.next = None  # Apunta al siguiente nodo en el caso de ser un nodo hoja

class BStarTree:
    def __init__(self, degree):
        self.degree = degree  # Grado mínimo del árbol B*
        self.root = BStarNode(is_leaf=True)  # Inicializa la raíz como un nodo hoja

    def search(self, id, node=None):
        # Busca un nodo con la clave id y retorna el nombre asociado si se encuentra
        if node is None:
            node = self.root  # Empieza la búsqueda desde la raíz
        i = 0
        while i < len(node.keys) and id > node.keys[i].id:
            i += 1
        if node.is_leaf:
            if i < len(node.keys) and node.keys[i].id == id:
                return node.keys[i].name  # Retorna el nombre si se encuentra la clave
            return None  # Retorna None si la clave no se encuentra
        else:
            if i < len(node.keys) and node.keys[i].id == id:
                return node.keys[i].name  # Retorna el nombre si se encuentra la clave
            return self.search(id, node.children[i])  # Continua la búsqueda en el hijo adecuado

    def insert(self, id, name):
        # Inserta una nueva clave en el árbol
        root = self.root
        if len(root.keys) == (2 * self.degree - 1):
            # Si el nodo raíz está lleno, crea una nueva raíz
            new_root = BStarNode()
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root  # Actualiza la raíz del árbol
        self._insert_non_full(self.root, id, name)

    def delete(self, id):
        # Elimina una clave del árbol
        root = self.root
        self._delete(root, id)
        if len(root.keys) == 0 and not root.is_leaf:
            self.root = root.children[0]  # Actualiza la raíz si está vacía

    def _delete(self, node, id):
        # Elimina una clave del nodo dado y maneja los casos de subárboles
        i = 0
        while i < len(node.keys) and node.keys[i].id < id:
            i += 1

        if node.is_leaf:
            if i < len(node.keys) and node.keys[i].id == id:
                node.keys.pop(i)  # Elimina la clave del nodo hoja
                return True
            return False
        else:
            if i < len(node.keys) and node.keys[i].id == id:
                if len(node.children[i].keys) >= self.degree:
                    # Si el hijo tiene suficientes claves, usa el predecesor
                    pred = self._get_predecessor(node, i)
                    node.keys[i] = pred
                    self._delete(node.children[i], pred.id)
                elif len(node.children[i + 1].keys) >= self.degree:
                    # Si el siguiente hijo tiene suficientes claves, usa el sucesor
                    succ = self._get_successor(node, i)
                    node.keys[i] = succ
                    self._delete(node.children[i + 1], succ.id)
                else:
                    # Si no se pueden tomar prestadas claves, fusiona hijos
                    self._merge(node, i)
                    self._delete(node.children[i], id)
            else:
                # Verificación de que el hijo tenga suficientes claves antes de eliminar
                if len(node.children[i].keys) < self.degree:
                    self._fill(node, i)
                if i < len(node.children):
                    if i > len(node.keys):
                        self._delete(node.children[i - 1], id)
                    else:
                        self._delete(node.children[i], id)
        return True

    def _fill(self, node, index):
        # Verificación que el nodo tenga suficientes claves
        if index > 0 and len(node.children[index - 1].keys) > self.degree * 2 // 3:
            self._borrow_from_prev(node, index)
        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) > self.degree * 2 // 3:
            self._borrow_from_next(node, index)
        else:
            if index < len(node.children) - 1:
                self._merge(node, index)
            else:
                self._merge(node, index - 1)

    def _borrow_from_prev(self, node, index):
        # Pide prestadas claves del hermano izquierdo del nodo
        child = node.children[index]
        sibling = node.children[index - 1]

        child.keys.insert(0, node.keys[index - 1])
        node.keys[index - 1] = sibling.keys.pop()

        if not sibling.is_leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, node, index):
        # Pide prestadas claves del hermano derecho del nodo
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys[index])
        node.keys[index] = sibling.keys.pop(0)

        if not sibling.is_leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, node, index):
        # Fusiona el hijo en el índice con el siguiente hijo
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys.pop(index))
        child.keys.extend(sibling.keys)

        if not child.is_leaf:
            child.children.extend(sibling.children)
        
        node.children.pop(index + 1)

    def _get_predecessor(self, node, index):
        # Encuentra el predecesor del nodo en el índice dado
        current = node.children[index]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node, index):
        # Encuentra el sucesor del nodo en el índice dado
        current = node.children[index + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def split_child(self, parent, index):
        # Divide el hijo completo en el índice dado y actualiza el nodo padre
        degree = self.degree
        full_child = parent.children[index]
        new_child = BStarNode(is_leaf=full_child.is_leaf)

        mid = degree - 1
        parent.keys.insert(index, full_child.keys[mid])
        parent.children.insert(index + 1, new_child)

        new_child.keys = full_child.keys[mid + 1:]
        full_child.keys = full_child.keys[:mid]

        if not full_child.is_leaf:
            new_child.children = full_child.children[mid + 1:]
            full_child.children = full_child.children[:mid + 1]
        else:
            new_child.next = full_child.next
            full_child.next = new_child

    def _insert_non_full(self, node, id, name):
        # Inserta una nueva clave en un nodo que no está lleno
        if node.is_leaf:
            index = 0
            while index < len(node.keys) and id > node.keys[index].id:
                index += 1
            node.keys.insert(index, Node(id, name))
        else:
            index = 0
            while index < len(node.keys) and id > node.keys[index].id:
                index += 1
            if len(node.children[index].keys) == (2 * self.degree - 1):
                self.split_child(node, index)
                if id > node.keys[index].id:
                    index += 1
            self._insert_non_full(node.children[index], id, name)
