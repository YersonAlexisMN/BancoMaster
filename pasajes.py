class Pasaje:

    def __init__(self, id_pasaje: str, id_viaje: str, id_cliente: str, id_origen: str, id_destino: str, asiento: int, valor: int, estado: str) -> None:
        self.id_pasaje = id_pasaje
        self.id_viaje = id_viaje
        self.id_cliente = id_cliente
        self.id_origen = id_origen
        self.id_destino = id_destino
        self.asiento = asiento
        self.valor = valor
        self.estado = estado

    def aLinea(self) -> str:
        return ",".join([
            self.id_pasaje,
            self.id_viaje,
            self.id_cliente,
            self.id_origen,
            self.id_destino,
            str(self.asiento),
            str(self.valor),
            self.estado
        ])

def calcularPrecio(pos_origen: int, pos_destino: int, tarifa_base: int) -> int:
    tramos_usados = abs(pos_destino - pos_origen)
    precio = tarifa_base * (5 + tramos_usados) / 10

    return int(precio)
