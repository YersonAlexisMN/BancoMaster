# RF02 · Buses: registrar, listar, consultar y cambiar disponibilidad
from archivos import agregarRegistro, leerRegistros, reescribirArchivo
from bus import Bus
from config import (ARCHIVO_BUSES, ENCABEZADO_BUSES, ESTADO_DISPONIBLE,
                    ESTADO_NO_DISPONIBLE, CAPACIDAD_MAXIMA)
from entradas import confirmar, pedirEntero, pedirTexto
from listaenlazada import ListaEnlazada
from mensajes import advertencia, encabezado, error, exito, titulo


# ---------------- Datos ----------------

def cargarBuses() -> ListaEnlazada:
    """Lee el archivo y carga los buses en una lista enlazada (clave = id_bus)."""
    lista = ListaEnlazada()
    for datos in leerRegistros(ARCHIVO_BUSES, ENCABEZADO_BUSES):
        try:
            bus = Bus(datos[0], datos[1], int(datos[2]), datos[3])
            if not lista.agregar(bus.id_bus, bus):
                advertencia(f"ID de bus repetido en el archivo: {bus.id_bus}")
        except (ValueError, IndexError):
            advertencia(f"Línea inválida en buses: {datos}")
    return lista


def listarBuses() -> list[Bus]:
    return cargarBuses().recorrer()


def buscarxCodigo(id_bus: str) -> Bus | None:
    nodo = cargarBuses().buscarxCodigo(id_bus)
    if nodo is not None:
        return nodo.dato
    return None


def buscarxPatente(patente: str) -> Bus | None:
    patente = normalizarPatente(patente)
    for bus in listarBuses():
        if bus.patente == patente:
            return bus
    return None


def guardarBus(bus: Bus) -> bool:
    return agregarRegistro(ARCHIVO_BUSES, ENCABEZADO_BUSES, bus.aLinea())


def modificarBus(busModificado: Bus) -> bool:
    """Reemplaza el bus con el mismo ID y reescribe el archivo."""
    lineas = []
    for bus in listarBuses():
        if bus.id_bus == busModificado.id_bus:
            lineas.append(busModificado.aLinea())
        else:
            lineas.append(bus.aLinea())
    return reescribirArchivo(ARCHIVO_BUSES, ENCABEZADO_BUSES, lineas)


def capacidadBus(id_bus: str) -> int:
    """Capacidad del bus o 0 si no existe (lo usa RF05 para validar el asiento)."""
    bus = buscarxCodigo(id_bus)
    if bus is not None:
        return bus.capacidad
    return 0


# ---------------- Validaciones ----------------

def normalizarPatente(patente: str) -> str:
    """Quita espacios, guiones y puntos y la deja en mayúsculas."""
    patente = patente.upper()
    patente = patente.replace(" ", "").replace("-", "").replace(".", "")
    return patente


def validarPatente(patente: str) -> bool:
    """Formato antiguo AB1234 o nuevo BCDF12 (sin vocales)."""
    if len(patente) != 6:
        return False
    # Formato antiguo: 2 letras + 4 números
    if patente[0:2].isalpha() and patente[2:6].isdigit():
        return True
    # Formato nuevo: 4 consonantes + 2 números
    if patente[0:4].isalpha() and patente[4:6].isdigit():
        for letra in patente[0:4]:
            if letra in "AEIOU":
                return False
        return True
    return False


# ---------------- Opciones del menú ----------------

def registrarBus() -> None:
    titulo("Registrar bus")
    patente = normalizarPatente(pedirTexto("Ingrese patente (ej: BCDF12 o AB1234): "))

    if not validarPatente(patente):
        error("Patente inválida. Formatos aceptados: AB1234 o BCDF12")
        return
    if buscarxPatente(patente) is not None:
        error(f"Ya existe un bus con la patente {patente}")
        return

    capacidad = pedirEntero(f"Ingrese capacidad (1 a {CAPACIDAD_MAXIMA}): ", 1, CAPACIDAD_MAXIMA)

    if confirmar("¿El bus queda disponible?"):
        estado = ESTADO_DISPONIBLE
    else:
        estado = ESTADO_NO_DISPONIBLE

    id_bus = str(cargarBuses().mayorCodigo() + 1)
    bus = Bus(id_bus, patente, capacidad, estado)

    if guardarBus(bus):
        exito("Bus registrado correctamente!!!")
        print(bus.info())


def mostrarBuses() -> None:
    titulo("Listado de buses")
    buses = listarBuses()
    if len(buses) == 0:
        advertencia("No hay buses registrados")
        return
    encabezado("ID | PATENTE | CAPACIDAD | ESTADO")
    for bus in buses:
        print(bus)
    print(f"\nTotal: {len(buses)} buses")


def consultarBus() -> None:
    titulo("Consultar bus")
    buscado = pedirTexto("Ingrese ID o patente del bus: ")
    if buscado.isdigit():
        bus = buscarxCodigo(buscado)
    else:
        bus = buscarxPatente(buscado)

    if bus is None:
        error("Bus no encontrado")
    else:
        print(bus.info())


def cambiarEstado() -> None:
    titulo("Cambiar disponibilidad")
    id_bus = str(pedirEntero("Ingrese ID del bus: ", 1, 999999))
    bus = buscarxCodigo(id_bus)
    if bus is None:
        error("Bus no encontrado")
        return

    if bus.estaDisponible():
        nuevoEstado = ESTADO_NO_DISPONIBLE
    else:
        nuevoEstado = ESTADO_DISPONIBLE

    if confirmar(f"El bus {bus.patente} pasará a '{nuevoEstado}'. ¿Confirmar?"):
        bus.estado = nuevoEstado
        if modificarBus(bus):
            exito("Estado actualizado!!!")
            if nuevoEstado == ESTADO_NO_DISPONIBLE:
                advertencia("No se podrán programar viajes nuevos con este bus")
    else:
        advertencia("Operación cancelada")


def menuBuses() -> None:
    while True:
        titulo("Gestión de buses")
        print("""
    1. Registrar bus
    2. Listar buses
    3. Consultar bus
    4. Cambiar disponibilidad
    0. Volver""")
        op = input("Ingrese una opción: ")
        match op:
            case "1":
                registrarBus()
            case "2":
                mostrarBuses()
            case "3":
                consultarBus()
            case "4":
                cambiarEstado()
            case "0":
                break
            case other:
                error("Opción no válida!!!")
        input("Presione Enter para continuar...")
