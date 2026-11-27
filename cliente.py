class Cliente:
    id_cliente: str
    rut: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    contacto: str

    def __init__(self, id_cliente: str, rut: str, nombres: str,
                 apellido_paterno: str, apellido_materno: str, contacto: str) -> None:
        self.id_cliente = id_cliente
        self.rut = rut
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contacto = contacto

    def __str__(self) -> str:
        return (f"{self.id_cliente} | {self.rut} | {self.nombres} {self.apellido_paterno} "
                f"{self.apellido_materno} | {self.contacto}")

    def info(self) -> str:
        return f"""
        ID CLIENTE: {self.id_cliente}
        RUT: {self.rut}
        NOMBRES: {self.nombres}
        APELLIDO PATERNO: {self.apellido_paterno}
        APELLIDO MATERNO: {self.apellido_materno}
        CONTACTO: {self.contacto}"""

    def aLinea(self) -> str:
        """Formato para guardar en el archivo CSV."""
        return (f"{self.id_cliente},{self.rut},{self.nombres},{self.apellido_paterno},"
                f"{self.apellido_materno},{self.contacto}")
