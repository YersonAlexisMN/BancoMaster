class Cliente:

    def __init__(self, id_cliente: str, rut: str, nombres: str, apellido_paterno: str, apellido_materno: str, contacto: str) -> None:
        self.id_cliente = id_cliente
        self.rut = rut
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contacto = contacto

    def aLinea(self) -> str:
        return ",".join([
            self.id_cliente,
            self.rut,
            self.nombres,
            self.apellido_paterno,
            self.apellido_materno,
            self.contacto
        ])

    def info(self) -> str:
        return self.id_cliente + " - " + self.rut + " - " + self.nombres + " " + self.apellido_paterno + " " + self.apellido_materno + " - " + self.contacto