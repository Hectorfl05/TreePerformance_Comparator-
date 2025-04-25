class BNode:
    def __init__(self, d, leaf=False):
        self.d = d  # Grado mínimo del árbol B
        self.leaf = leaf  # Indica si el nodo es una hoja
        self.pairs = []  # Lista de pares (id, nombre)
        self.children = []  # Lista de hijos del nodo

class TreeB:
    def __init__(self, d):
        self.root = BNode(d, leaf=True)  # Inicializa la raíz del árbol como un nodo hoja
        self.d = d  # Grado mínimo del árbol B
    
    def insert(self, id, nombre):
        root = self.root
        # Si la raíz está llena, se divide
        if len(root.pairs) == (2 * self.d - 1):
            s = BNode(self.d, leaf=False)  # Nuevo nodo no hoja
            self.root = s
            s.children.append(root)
            self._split_child(s, 0)  # Divide el hijo de la raíz
            self._insert_non_full(s, id, nombre)  # Inserta en el nuevo nodo raíz
        else:
            self._insert_non_full(root, id, nombre)  # Inserta en la raíz
    
    def _insert_non_full(self, nodo, id, nombre):
        i = len(nodo.pairs) - 1
        nuevo_par = (id, nombre)
        if nodo.leaf:
            # Inserta en un nodo hoja
            nodo.pairs.append(None)
            while i >= 0 and nuevo_par < nodo.pairs[i]:
                nodo.pairs[i + 1] = nodo.pairs[i]
                i -= 1
            nodo.pairs[i + 1] = nuevo_par
        else:
            # Inserta en un nodo interno
            while i >= 0 and nuevo_par < nodo.pairs[i]:
                i -= 1
            i += 1
            # Si el hijo está lleno, se divide
            if len(nodo.children[i].pairs) == (2 * self.d - 1):
                self._split_child(nodo, i)
                if nuevo_par > nodo.pairs[i]:
                    i += 1
            self._insert_non_full(nodo.children[i], id, nombre)
    
    def _split_child(self, nodo, i):
        d = self.d
        y = nodo.children[i]
        z = BNode(d, leaf=y.leaf)  # Nuevo nodo para la división
        nodo.children.insert(i + 1, z)  # Inserta el nuevo hijo
        nodo.pairs.insert(i, y.pairs[d - 1])  # Mueve la clave del medio al nodo padre
        z.pairs = y.pairs[d:(2 * d - 1)]  # Asigna los pares al nuevo nodo
        y.pairs = y.pairs[0:(d - 1)]  # Ajusta los pares del nodo original
        if not y.leaf:
            z.children = y.children[d:(2 * d)]  # Mueve los hijos al nuevo nodo
            y.children = y.children[0:d]
    
    def search(self, id):
        return self._search(self.root, id)
    
    def _search(self, nodo, id):
        i = 0
        # Busca el índice donde podría estar el id
        while i < len(nodo.pairs) and id > nodo.pairs[i][0]:
            i += 1
        if i < len(nodo.pairs) and id == nodo.pairs[i][0]:
            return nodo.pairs[i][1]  # Retorna el nombre si se encuentra el id
        if nodo.leaf:
            return None  # Retorna None si no se encontró la id
        return self._search(nodo.children[i], id)
    
    def delete(self, id):
        eliminado, self.root = self._delete(self.root, id)
        # Si la raíz quedó vacía, se actualiza la raíz
        if len(self.root.pairs) == 0 and not self.root.leaf:
            self.root = self.root.children[0]
        return eliminado
    
    def _delete(self, nodo, id):
        if nodo.leaf:
            # Eliminar un par de un nodo hoja
            for i, par in enumerate(nodo.pairs):
                if par[0] == id:
                    nombre = par[1]
                    nodo.pairs.pop(i)
                    return nombre, nodo
            return None, nodo
        
        # Buscar el índice del hijo donde se debería eliminar el id
        i = 0
        while i < len(nodo.pairs) and id > nodo.pairs[i][0]:
            i += 1
        
        if i < len(nodo.pairs) and id == nodo.pairs[i][0]:
            # Eliminar un par de un nodo no hoja
            if len(nodo.children[i].pairs) >= self.d:
                pred = self._get_predecesor(nodo.children[i])
                pred_id = pred[0]
                pred_nombre = pred[1]
                self._delete(nodo.children[i], pred_id)
                nodo.pairs[i] = (pred_id, pred_nombre)
            elif len(nodo.children[i + 1].pairs) >= self.d:
                succ = self._get_sucesor(nodo.children[i + 1])
                succ_id = succ[0]
                succ_nombre = succ[1]
                self._delete(nodo.children[i + 1], succ_id)
                nodo.pairs[i] = (succ_id, succ_nombre)
            else:
                # Fusión de los hijos y eliminación el id
                self._merge_children(nodo, i)
                self._delete(nodo.children[i], id)
        else:
            # Verificacion de que el hijo tenga suficientes pares antes de eliminar
            if len(nodo.children[i].pairs) == self.d - 1:
                if i > 0 and len(nodo.children[i - 1].pairs) >= self.d:
                    self._borrow_from_prev(nodo, i)
                elif i < len(nodo.children) - 1 and len(nodo.children[i + 1].pairs) >= self.d:
                    self._borrow_from_next(nodo, i)
                else:
                    if i < len(nodo.children) - 1:
                        self._merge_children(nodo, i)
                    else:
                        self._merge_children(nodo, i - 1)
                        i -= 1
            self._delete(nodo.children[i], id)
        
        # Si la raíz quedó vacía, se actualiza la raíz
        if len(self.root.pairs) == 0:
            self.root = self.root.children[0] if self.root.children else BNode(self.d, leaf=True)
        
        return None, nodo
    
    def _get_predecesor(self, nodo):
        # Encuentra el predecesor (el par más grande en el subárbol)
        while not nodo.leaf:
            nodo = nodo.children[-1]
        return nodo.pairs[-1]
    
    def _get_sucesor(self, nodo):
        # Encuentra el sucesor (el par más pequeño en el subárbol)
        while not nodo.leaf:
            nodo = nodo.children[0]
        return nodo.pairs[0]
    
    def _merge_children(self, nodo, i):
        # Fusiona el hijo en la posición i con el hermano derecho
        child = nodo.children[i]
        sibling = nodo.children[i + 1]
        child.pairs.append(nodo.pairs[i])
        child.pairs.extend(sibling.pairs)
        if not child.leaf:
            child.children.extend(sibling.children)
        nodo.pairs.pop(i)
        nodo.children.pop(i + 1)
    
    def _borrow_from_prev(self, nodo, i):
        # Pide prestado un par del hermano izquierdo
        child = nodo.children[i]
        sibling = nodo.children[i - 1]
        child.pairs.insert(0, nodo.pairs[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        nodo.pairs[i - 1] = sibling.pairs.pop()
    
    def _borrow_from_next(self, nodo, i):
        # Pide prestado un par del hermano derecho
        child = nodo.children[i]
        sibling = nodo.children[i + 1]
        child.pairs.append(nodo.pairs[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        nodo.pairs[i] = sibling.pairs.pop(0)
