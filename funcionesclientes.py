from cliente import Cliente
from archivos import leerRegistros
from config import ARCHIVO_CLIENTES, ENCABEZADO_CLIENTES
from archivos import agregarRegistro
from entradas import pedirTexto
from archivos import reescribirArchivo



def cargarClientes() -> list[Cliente]:

    registros = leerRegistros(
        ARCHIVO_CLIENTES,
        ENCABEZADO_CLIENTES
    )

    clientes = []

    for registro in registros:

        cliente = Cliente(
            registro[0],
            registro[1],
            registro[2],
            registro[3],
            registro[4],
            registro[5]
        )

        clientes.append(cliente)

    return clientes

def buscarxCodigo(id_cliente: str) -> Cliente | None:

    clientes = cargarClientes()

    for cliente in clientes:

        if cliente.id_cliente == id_cliente:
            return cliente

    return None

def buscarxRut(rut: str) -> Cliente | None:

    clientes = cargarClientes()

    for cliente in clientes:

        if cliente.rut == rut:
            return cliente

    return None


def listarClientes() -> None:

    clientes = cargarClientes()

    if len(clientes) == 0:
        print("NO HAY CLIENTES")
        return

    for cliente in clientes:
        print(cliente.info())


def guardarCliente(cliente: Cliente) -> bool:

    return agregarRegistro(
        ARCHIVO_CLIENTES,
        ENCABEZADO_CLIENTES,
        cliente.aLinea()
    )

def registrarCliente() -> None:

    id_cliente = pedirTexto("ID Cliente: ")
    rut = pedirTexto("RUT: ")
    if buscarxRut(rut) is not None:
        print("ERROR: RUT YA REGISTRADO")
        return
    nombres = pedirTexto("Nombres: ")
    apellido_paterno = pedirTexto("Apellido paterno: ")
    apellido_materno = pedirTexto("Apellido materno: ")
    contacto = pedirTexto("Contacto: ")

    cliente = Cliente(
        id_cliente,
        rut,
        nombres,
        apellido_paterno,
        apellido_materno,
        contacto
    )

    guardarCliente(cliente)

    print("CLIENTE REGISTRADO")


def modificarCliente() -> None:

    id_cliente = pedirTexto(
        "Ingrese ID del cliente: "
    )

    clientes = cargarClientes()

    encontrado = False

    for cliente in clientes:

        if cliente.id_cliente == id_cliente:

            cliente.rut = pedirTexto("Nuevo RUT: ")
            cliente.nombres = pedirTexto("Nuevos nombres: ")
            cliente.apellido_paterno = pedirTexto(
                "Nuevo apellido paterno: "
            )
            cliente.apellido_materno = pedirTexto(
                "Nuevo apellido materno: "
            )
            cliente.contacto = pedirTexto(
                "Nuevo contacto: "
            )

            encontrado = True
            break

    if not encontrado:
        print("CLIENTE NO EXISTE")
        return

    lineas = []

    for cliente in clientes:
        lineas.append(cliente.aLinea())

    reescribirArchivo(
        ARCHIVO_CLIENTES,
        ENCABEZADO_CLIENTES,
        lineas
    )

    print("CLIENTE MODIFICADO")

def buscarxRut(rut: str):

    clientes = cargarClientes()

    for cliente in clientes:

        if cliente.rut == rut:
            return cliente

    return None

def menuClientes() -> None:

    while True:

        print("\n--- CLIENTES ---")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Modificar cliente")
        print("4. Volver")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrarCliente()

        elif opcion == "2":
            listarClientes()

        elif opcion == "3":
            modificarCliente()

        elif opcion == "4":
            break