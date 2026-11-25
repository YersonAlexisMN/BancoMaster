class Ciudad:
    id_ciudad: str
    nombre: str
    posicion: int

    def __init__(self, id_ciudad: str, nombre: str, posicion: int) -> None:
        self.id_ciudad = id_ciudad
        self.nombre = nombre
        self.posicion = posicion

    def __str__(self) -> str:
        return f"{self.id_ciudad} | {self.nombre} | posición {self.posicion}"

    def info(self) -> str:
        return f"""
        ID CIUDAD: {self.id_ciudad}
        NOMBRE: {self.nombre}
        POSICIÓN: {self.posicion}"""

    def aLinea(self) -> str:
        return f"{self.id_ciudad},{self.nombre},{self.posicion}"
