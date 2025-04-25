from __future__ import print_function

# Definición de la clase Nodo para el árbol AVL
class Node2:
    def __init__(self, label, name: str):
        self.label = label  # Etiqueta del nodo (ID)
        self.name = name  # Nombre del nodo
        self._parent = None  # Referencia al padre del nodo
        self._left = None  # Referencia al hijo izquierdo del nodo
        self._right = None  # Referencia al hijo derecho del nodo
        self.height = 0  # Altura del nodo

    # Propiedad para acceder al hijo derecho
    @property
    def right(self):
        return self._right

    # Setter del hijo derecho
    @right.setter
    def right(self, node):
        if node is not None:
            node._parent = self
        self._right = node

    # Propiedad para acceder al hijo izquierdo
    @property
    def left(self):
        return self._left

    # Setter del hijo izquierdo
    @left.setter
    def left(self, node):
        if node is not None:
            node._parent = self
        self._left = node

    # Propiedad para acceder al nodo padre
    @property
    def parent(self):
        return self._parent

    # Setter del nodo padre
    @parent.setter
    def parent(self, node):
        self._parent = node
        if node is not None:
            self.height = self.parent.height + 1  # Actualiza la altura del nodo actual
        else:
            self.height = 0  # Si el nodo dado es None, la altura se vuelve a 0

class AVL2:
    def __init__(self):
        self.root = None  # Nodo raíz
        self.size = 0  # Tamaño inicial del árbol

    def insert(self, value, n: str):
        node = Node2(value, n)  # Se crea un nuevo nodo con los atributos dados

        if self.root is None:
            self.root = node  # Si el árbol está vacío, se crea el nodo raíz
            self.root.height = 0  # Se inicializa la altura de la raíz como 0
            self.size = 1  # Se actualiza el tamaño del árbol
        else:
            dad_node = None
            curr_node = self.root  # Se ubica en el nodo raíz

            while True:
                if curr_node is not None:  # Condición que verifica que el nodo actual exista
                    dad_node = curr_node  # Establece el nodo actual como nodo padre
                    if node.label < curr_node.label:
                        curr_node = curr_node.left  # Se desplaza hacia la izquierda, si la ID es menor
                    else:
                        curr_node = curr_node.right  # Se desplaza hacia la derecha del árbol, si la ID es mayor
                else:
                    node.height = dad_node.height
                    dad_node.height += 1  # Se actualiza la altura de los nodos
                    if node.label < dad_node.label:  # Se verifica si la ID del nodo es menor o mayor que la del padre
                        dad_node.left = node  # Se inserta como hijo izquierdo
                    else:
                        dad_node.right = node  # Se inserta como hijo derecho
                    self.rebalance(node)  # Se rebalancea el árbol
                    self.size += 1  # Se aumenta el tamaño del árbol
                    break

    def rebalance(self, node):
        n = node

        while n is not None:  # Loop que itera hasta que el nodo actual sea nulo
            height_right = n.right.height if n.right is not None else 0
            height_left = n.left.height if n.left is not None else 0

            if abs(height_left - height_right) > 1:  # Se verifica si la diferencia de altura es mayor que 1
                if height_left > height_right:
                    left_child = n.left
                    h_right = left_child.right.height if left_child.right is not None else 0
                    h_left = left_child.left.height if left_child.left is not None else 0
                    if h_left > h_right:  # Si la altura izquierda es mayor que la derecha
                        self.rotate_right(n)  # Rotación simple a la derecha
                    else:
                        self.double_rotate_right(n)  # Rotación doble a la derecha
                else:
                    right_child = n.right
                    h_right = right_child.right.height if right_child.right is not None else 0
                    h_left = right_child.left.height if right_child.left is not None else 0
                    if h_left > h_right:  # Si la altura izquierda es mayor que la derecha
                        self.double_rotate_left(n)  # Rotación doble a la izquierda
                    else:
                        self.rotate_left(n)  # Rotación simple a la izquierda
                break
            n = n.parent

    def rotate_left(self, node):
        # Realiza una rotación a la izquierda en el nodo dado.
        new_root = node.right
        if new_root is None:
            return  # No se puede realizar la rotación si no hay hijo derecho

        # Reasigna los hijos del nuevo nodo raíz
        node.right = new_root.left
        if new_root.left is not None:
            new_root.left.parent = node
        new_root.parent = node.parent
        
        # Actualiza el padre del nuevo nodo raíz
        if node.parent is None:
            self.root = new_root  # Si el nodo es la raíz, actualiza la raíz del árbol
        elif node == node.parent.left:
            node.parent.left = new_root  # El nodo original es hijo izquierdo
        else:
            node.parent.right = new_root  # El nodo original es hijo derecho
        
        # Completa la rotación
        new_root.left = node
        node.parent = new_root

    def rotate_right(self, node):
        # Realiza una rotación a la derecha en el nodo dado.
        new_root = node.left
        if new_root is None:
            return  # No se puede realizar la rotación si no hay hijo izquierdo

        # Reasigna los hijos del nuevo nodo raíz
        node.left = new_root.right
        if new_root.right is not None:
            new_root.right.parent = node
        new_root.parent = node.parent
        
        # Actualiza el padre del nuevo nodo raíz
        if node.parent is None:
            self.root = new_root  # Si el nodo es la raíz, actualiza la raíz del árbol
        elif node == node.parent.right:
            node.parent.right = new_root  # El nodo original es hijo derecho
        else:
            node.parent.left = new_root  # El nodo original es hijo izquierdo
        
        # Completa la rotación
        new_root.right = node
        node.parent = new_root

    def double_rotate_left(self, node):
        # Realiza una rotación doble a la izquierda en el nodo dado.
        # Primero rota a la derecha en el hijo derecho del nodo
        if node.right is not None:
            self.rotate_right(node.right)
        # Luego rota a la izquierda en el nodo original
        self.rotate_left(node)

    def double_rotate_right(self, node):
        # Realiza una rotación doble a la derecha en el nodo dado.
        # Primero rota a la izquierda en el hijo izquierdo del nodo
        if node.left is not None:
            self.rotate_left(node.left)
        # Luego rota a la derecha en el nodo original
        self.rotate_right(node)

    def search(self, value):
        # Busca un valor en el árbol y retorna el nodo y un booleano indicando si se encontró.
        current = self.root
        while current is not None:
            if value == current.label:
                return current, True  # Retorna el nodo y True si se encontró el valor
            elif value < current.label:
                current = current.left  # Busca en el subárbol izquierdo
            else:
                current = current.right  # Busca en el subárbol derecho
        return None, False  # Retorna None y False si el valor no se encontró


    def delete(self, value):
        node, found = self.search(value)  # Busca el nodo a eliminar
        if not found:
            return None, False

        self._delete_node(node)
        self.size -= 1
        return node, True

    def _delete_node(self, node):
        if node.left is None and node.right is None:
            # Caso 1: El nodo no tiene hijos
            self._replace_node_in_parent(node, None)
        elif node.left is None:
            # Caso 2: El nodo tiene un solo hijo (derecho)
            self._replace_node_in_parent(node, node.right)
        elif node.right is None:
            # Caso 2: El nodo tiene un solo hijo (izquierdo)
            self._replace_node_in_parent(node, node.left)
        else:
            # Caso 3: El nodo tiene dos hijos
            # Encuentra el sucesor inorder (el nodo más pequeño en el subárbol derecho)
            successor = self._find_min(node.right)
            node.label = successor.label
            node.name = successor.name
            self._delete_node(successor)  # Elimina el sucesor

        # Rebala el árbol a partir del padre del nodo eliminado
        self.rebalance(node.parent)

    def _replace_node_in_parent(self, node, new_value):
        if node.parent is not None:
            if node == node.parent.left:
                node.parent.left = new_value
            else:
                node.parent.right = new_value
        else:
            self.root = new_value
        if new_value is not None:
            new_value.parent = node.parent

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
