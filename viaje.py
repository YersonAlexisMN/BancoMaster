from datetime import datetime


class Viaje:
    id_viaje: str
    id_bus: str
    fecha: str
    hora: str
    id_origen: str
    id_destino: str
    tarifa_base: int

    def __init__(self, id_viaje: str, id_bus: str, fecha: str, hora: str,
                 id_origen: str, id_destino: str, tarifa_base: int) -> None:
        self.id_viaje = id_viaje
        self.id_bus = id_bus
        self.fecha = fecha
        self.hora = hora
        self.id_origen = id_origen
        self.id_destino = id_destino
        self.tarifa_base = tarifa_base

    def __str__(self) -> str:
        return (f"{self.id_viaje} | {self.fecha} {self.hora} | bus {self.id_bus} | "
                f"{self.id_origen} -> {self.id_destino} | ${self.tarifa_base}")

    def fechaHora(self) -> datetime:
        return datetime.strptime(self.fecha + " " + self.hora, "%Y-%m-%d %H:%M")

    def aLinea(self) -> str:
        return (f"{self.id_viaje},{self.id_bus},{self.fecha},{self.hora},"
                f"{self.id_origen},{self.id_destino},{self.tarifa_base}")
