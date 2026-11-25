# Lista enlazada simple: cada nodo guarda un código (ID) y el objeto (Bus, Viaje, etc.)
# Se usa para cargar los registros del archivo y buscarlos por código sin repetir IDs.


class Nodo:
    def __init__(self, codigo: str, dato: object) -> None:
        self.codigo = codigo
        self.dato = dato
        self.siguiente = None

    def __str__(self) -> str:
        return self.codigo + " | " + str(self.dato)


class ListaEnlazada:
    def __init__(self) -> None:
        self.inicio = None
        self.cantidad = 0

    def estaVacia(self) -> bool:
        return self.inicio is None

    def agregar(self, codigo: str, dato: object) -> bool:
        """Agrega al final. Si el código ya existe, no lo agrega y devuelve False."""
        buscar = self.buscarxCodigo(codigo)
        if buscar is not None:
            return False

        nodonuevo = Nodo(codigo, dato)

        if self.inicio is None:
            self.inicio = nodonuevo
        else:
            puntero = self.inicio
            while puntero.siguiente is not None:
                puntero = puntero.siguiente
            puntero.siguiente = nodonuevo

        self.cantidad += 1
        return True

    def buscarxCodigo(self, codigoBuscado: str) -> Nodo | None:
        puntero = self.inicio
        while puntero is not None:
            if puntero.codigo == codigoBuscado:
                return puntero
            else:
                puntero = puntero.siguiente
        return None

    def recorrer(self) -> list:
        """Devuelve los datos de todos los nodos en orden."""
        datos = []
        puntero = self.inicio
        while puntero is not None:
            datos.append(puntero.dato)
            puntero = puntero.siguiente
        return datos

    def mayorCodigo(self) -> int:
        """Recorre la lista y devuelve el código numérico más alto (0 si está vacía)."""
        mayor = 0
        puntero = self.inicio
        while puntero is not None:
            if puntero.codigo.isdigit() and int(puntero.codigo) > mayor:
                mayor = int(puntero.codigo)
            puntero = puntero.siguiente
        return mayor
