from node import Node

class BPlusNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf  # Indica si el nodo es una hoja
        self.keys = []  # Lista de claves, cada clave es una instancia de Node
        self.children = []  # Lista de hijos del nodo
        self.next = None  # Solo se usa si el nodo es una hoja para enlazar con el siguiente nodo hoja

class BPlusTree:
    def __init__(self, degree):
        self.degree = degree  # Grado mínimo del árbol B+
        self.root = BPlusNode(is_leaf=True)  # Inicializa la raíz del árbol como un nodo hoja

    def search(self, id, node=None):
        # Busca un id en el árbol B+
        if node is None:
            node = self.root  # Comienza la búsqueda en la raíz
        i = 0
        # Encuentra el índice del primer nodo con clave mayor o igual a id
        while i < len(node.keys) and id > node.keys[i].id:
            i += 1
        if node.is_leaf:
            # Si se encuentra en una hoja, verifica si la clave está presente
            if i < len(node.keys) and node.keys[i].id == id:
                return node.keys[i].name
            return None
        else:
            # Si no es una hoja, busca recursivamente en el hijo adecuado
            if i < len(node.keys) and node.keys[i].id == id:
                return node.keys[i].name
            return self.search(id, node.children[i])

    def insert(self, id, name):
        # Inserta un nuevo par (id, name) en el árbol B+
        root = self.root
        # Si la raíz está llena, debe dividirse
        if len(root.keys) == (2 * self.degree - 1):
            new_root = BPlusNode()  # Crea una nueva raíz
            new_root.children.append(self.root)  # Mueve la antigua raíz a los hijos de la nueva raíz
            self.split_child(new_root, 0)  # Divide el hijo lleno
            self.root = new_root  # Actualiza la raíz del árbol
        self._insert_non_full(self.root, id, name)  # Inserta el nuevo par en el árbol

    def delete(self, id):
        # Elimina un par (id, name) del árbol B+
        root = self.root
        self._delete(root, id)
        # Si la raíz queda vacía y no es hoja, actualiza la raíz
        if len(root.keys) == 0 and not root.is_leaf:
            self.root = root.children[0]

    def _delete(self, node, id):
        # Elimina una clave (id) en un nodo
        i = 0
        # Encuentra el índice del primer nodo con clave mayor o igual a id
        while i < len(node.keys) and node.keys[i].id < id:
            i += 1

        if node.is_leaf:
            # Elimina la clave en una hoja
            if i < len(node.keys) and node.keys[i].id == id:
                node.keys.pop(i)
                return True
            return False
        else:
            # Si el nodo tiene la clave, maneja los casos de claves en hijos
            if i < len(node.keys) and node.keys[i].id == id:
                if len(node.children[i].keys) >= self.degree:
                    pred = self._get_predecessor(node, i)  # Encuentra el predecesor
                    node.keys[i] = pred
                    self._delete(node.children[i], pred.id)  # Elimina la clave en el hijo
                elif len(node.children[i + 1].keys) >= self.degree:
                    succ = self._get_successor(node, i)  # Encuentra el sucesor
                    node.keys[i] = succ
                    self._delete(node.children[i + 1], succ.id)  # Elimina la clave en el hijo
                else:
                    # Si ambos hijos tienen menos de d claves, fusiona los hijos
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
        # Llena un hijo que tiene menos de d claves pidiendo prestado de hermanos
        if index > 0 and len(node.children[index - 1].keys) >= self.degree:
            self._borrow_from_prev(node, index)  # Presta del hermano izquierdo
        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) >= self.degree:
            self._borrow_from_next(node, index)  # Presta del hermano derecho
        else:
            # Fusiona con el hermano izquierdo o derecho
            if index < len(node.children) - 1:
                self._merge(node, index)
            else:
                self._merge(node, index - 1)

    def _borrow_from_prev(self, node, index):
        # Presta una clave del hermano izquierdo
        child = node.children[index]
        sibling = node.children[index - 1]

        child.keys.insert(0, node.keys[index - 1])
        node.keys[index - 1] = sibling.keys.pop()

        if not sibling.is_leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, node, index):
        # Presta una clave del hermano derecho
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys[index])
        node.keys[index] = sibling.keys.pop(0)

        if not sibling.is_leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, node, index):
        # Fusiona el hijo en la posición index con el hermano derecho
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys.pop(index))
        child.keys.extend(sibling.keys)

        if not child.is_leaf:
            child.children.extend(sibling.children)
        
        node.children.pop(index + 1)

    def _get_predecessor(self, node, index):
        # Encuentra el predecesor (la clave más grande en el hijo izquierdo)
        current = node.children[index]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node, index):
        # Encuentra el sucesor (la clave más pequeña en el hijo derecho)
        current = node.children[index + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def split_child(self, parent, index):
        # Divide un hijo del nodo padre y ajusta las claves y los hijos
        degree = self.degree
        full_child = parent.children[index]
        new_child = BPlusNode(is_leaf=full_child.is_leaf)

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
        # Inserta una clave en un nodo que no está lleno
        if node.is_leaf:
            index = 0
            while index < len(node.keys) and id > node.keys[index].id:
                index += 1
            node.keys.insert(index, Node(id, name))
        else:
            index = 0
            while index < len(node.keys) and id > node.keys[index].id:
                index += 1
            # Si el hijo está lleno, se divide
            if len(node.children[index].keys) == (2 * self.degree - 1):
                self.split_child(node, index)
                if id > node.keys[index].id:
                    index += 1
            self._insert_non_full(node.children[index], id, name)
