from config import ESTADO_DISPONIBLE


class Bus:
    id_bus: str
    patente: str
    capacidad: int
    estado: str

    def __init__(self, id_bus: str, patente: str, capacidad: int, estado: str) -> None:
        self.id_bus = id_bus
        self.patente = patente
        self.capacidad = capacidad
        self.estado = estado

    def __str__(self) -> str:
        return f"{self.id_bus} | {self.patente} | {self.capacidad} asientos | {self.estado}"

    def info(self) -> str:
        return f"""
        ID BUS: {self.id_bus}
        PATENTE: {self.patente}
        CAPACIDAD: {self.capacidad} asientos
        ESTADO: {self.estado}"""

    def estaDisponible(self) -> bool:
        return self.estado == ESTADO_DISPONIBLE

    def aLinea(self) -> str:
        """Formato para guardar en el archivo CSV."""
        return f"{self.id_bus},{self.patente},{self.capacidad},{self.estado}"
