class Cliente:

    def __init__(
        self,
        id_cliente: str,
        rut: str,
        nombres: str,
        apellido_paterno: str,
        apellido_materno: str,
        contacto: str
    ):
        self.id_cliente = id_cliente
        self.rut = rut
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contacto = contacto

    def __str__(self) -> str:
        return self.info()

    def info(self) -> str:
        return (
            f"{self.id_cliente} | "
            f"{self.rut} | "
            f"{self.nombres} "
            f"{self.apellido_paterno} "
            f"{self.apellido_materno}"
        )

def aLinea(self) -> str:
    return (
        f"{self.id_cliente},"
        f"{self.rut},"
        f"{self.nombres},"
        f"{self.apellido_paterno},"
        f"{self.apellido_materno},"
        f"{self.contacto}"
    )
