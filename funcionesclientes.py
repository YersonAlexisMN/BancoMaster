# RF01 · Clientes: registrar, listar, buscar y modificar
from archivos import agregarRegistro, leerRegistros, reescribirArchivo
from cliente import Cliente
from config import ARCHIVO_CLIENTES, ENCABEZADO_CLIENTES
from entradas import confirmar, pedirTexto
from listaenlazada import ListaEnlazada
from mensajes import advertencia, encabezado, error, exito, titulo


# ---------------- Datos ----------------

def cargarClientes() -> ListaEnlazada:
    """Lee el archivo y carga los clientes en una lista enlazada (clave = id_cliente)."""
    lista = ListaEnlazada()
    for datos in leerRegistros(ARCHIVO_CLIENTES, ENCABEZADO_CLIENTES):
        try:
            cliente = Cliente(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5])
            if not lista.agregar(cliente.id_cliente, cliente):
                advertencia(f"ID de cliente repetido en el archivo: {cliente.id_cliente}")
        except IndexError:
            advertencia(f"Línea inválida en clientes: {datos}")
    return lista


def listarTodos() -> list[Cliente]:
    return cargarClientes().recorrer()


def buscarxCodigo(id_cliente: str) -> Cliente | None:
    """Devuelve el Cliente o None (lo usa pasajes para validar la venta)."""
    nodo = cargarClientes().buscarxCodigo(id_cliente)
    if nodo is not None:
        return nodo.dato
    return None


def buscarxRut(rut: str) -> Cliente | None:
    rut = normalizarRut(rut)
    for cliente in listarTodos():
        if cliente.rut == rut:
            return cliente
    return None


def guardarCliente(cliente: Cliente) -> bool:
    return agregarRegistro(ARCHIVO_CLIENTES, ENCABEZADO_CLIENTES, cliente.aLinea())


def reescribirClientes(clientes: list[Cliente]) -> bool:
    lineas = []
    for cliente in clientes:
        lineas.append(cliente.aLinea())
    return reescribirArchivo(ARCHIVO_CLIENTES, ENCABEZADO_CLIENTES, lineas)


# ---------------- Validaciones ----------------

def normalizarRut(rut: str) -> str:
    """Quita puntos y espacios, deja la K en mayúscula y el formato 12345678-5."""
    rut = rut.upper().replace(".", "").replace(" ", "").replace("-", "")
    if len(rut) < 2:
        return rut
    return rut[:-1] + "-" + rut[-1]


def calcularDigitoVerificador(numero: str) -> str:
    """Algoritmo módulo 11 del RUT chileno."""
    suma = 0
    multiplicador = 2
    for digito in reversed(numero):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    elif resto == 10:
        return "K"
    else:
        return str(resto)


def validarRut(rut: str) -> bool:
    """El rut debe venir normalizado: 12345678-5."""
    if "-" not in rut:
        return False
    numero, dv = rut.split("-")
    if not numero.isdigit() or len(numero) < 7 or len(numero) > 8:
        return False
    return calcularDigitoVerificador(numero) == dv


def pedirNombre(mensaje: str) -> str:
    """Pide un nombre o apellido sin números ni comas (la coma rompería el CSV)."""
    while True:
        texto = pedirTexto(mensaje)
        if "," in texto:
            error("No puede contener comas")
        elif any(c.isdigit() for c in texto):
            error("No puede contener números")
        else:
            return texto.title()


def pedirContacto(mensaje: str) -> str:
    while True:
        texto = pedirTexto(mensaje)
        if "," in texto:
            error("No puede contener comas")
        else:
            return texto


# ---------------- Opciones del menú ----------------

def registrarCliente() -> None:
    titulo("Registrar cliente")
    rut = normalizarRut(pedirTexto("Ingrese RUT (ej: 12.345.678-5): "))

    if not validarRut(rut):
        error("RUT inválido, revise el número y el dígito verificador")
        return
    if buscarxRut(rut) is not None:
        error(f"Ya existe un cliente con el RUT {rut}. Registro rechazado")
        return

    nombres = pedirNombre("Ingrese nombres: ")
    apellido_paterno = pedirNombre("Ingrese apellido paterno: ")
    apellido_materno = pedirNombre("Ingrese apellido materno: ")
    contacto = pedirContacto("Ingrese contacto (teléfono o correo): ")

    id_cliente = str(cargarClientes().mayorCodigo() + 1)
    cliente = Cliente(id_cliente, rut, nombres, apellido_paterno, apellido_materno, contacto)

    if guardarCliente(cliente):
        exito("Cliente registrado correctamente!!!")
        print(cliente.info())


def mostrarClientes() -> None:
    titulo("Listado de clientes")
    clientes = listarTodos()
    if len(clientes) == 0:
        advertencia("No hay clientes registrados")
        return
    encabezado("ID | RUT | NOMBRE COMPLETO | CONTACTO")
    for cliente in clientes:
        print(cliente)
    print(f"\nTotal: {len(clientes)} clientes")


def consultarCliente() -> None:
    titulo("Buscar cliente")
    buscado = pedirTexto("Ingrese ID o RUT del cliente: ")
    if buscado.isdigit() and len(buscado) <= 6:
        cliente = buscarxCodigo(buscado)
    else:
        cliente = buscarxRut(buscado)

    if cliente is None:
        error("Cliente no encontrado")
    else:
        print(cliente.info())


def modificarCliente() -> None:
    titulo("Modificar cliente")
    id_cliente = pedirTexto("Ingrese ID del cliente: ")
    clientes = listarTodos()

    for cliente in clientes:
        if cliente.id_cliente == id_cliente:
            print(cliente.info())
            print("\n    Escriba x para mantener el dato actual")

            nombres = input("Nuevos nombres: ").strip()
            if nombres.lower() != "x" and nombres != "" and "," not in nombres:
                cliente.nombres = nombres.title()

            paterno = input("Nuevo apellido paterno: ").strip()
            if paterno.lower() != "x" and paterno != "" and "," not in paterno:
                cliente.apellido_paterno = paterno.title()

            materno = input("Nuevo apellido materno: ").strip()
            if materno.lower() != "x" and materno != "" and "," not in materno:
                cliente.apellido_materno = materno.title()

            contacto = input("Nuevo contacto: ").strip()
            if contacto.lower() != "x" and contacto != "" and "," not in contacto:
                cliente.contacto = contacto

            if confirmar("¿Guardar cambios?"):
                if reescribirClientes(clientes):
                    exito("Cliente modificado!!!")
                    print(cliente.info())
            else:
                advertencia("Operación cancelada")
            return

    error("Cliente no encontrado")


def menuClientes() -> None:
    while True:
        titulo("Gestión de clientes")
        print("""
    1. Registrar cliente
    2. Listar clientes
    3. Buscar cliente
    4. Modificar cliente
    0. Volver""")
        op = input("Ingrese una opción: ")
        match op:
            case "1":
                registrarCliente()
            case "2":
                mostrarClientes()
            case "3":
                consultarCliente()
            case "4":
                modificarCliente()
            case "0":
                break
            case other:
                error("Opción no válida!!!")
        input("Presione Enter para continuar...")
