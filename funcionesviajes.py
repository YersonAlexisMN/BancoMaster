# RF04 · Viajes: programar, listar y consultar
from datetime import datetime

import funcionesbuses
import funcionesciudades
from archivos import agregarRegistro, leerRegistros
from config import (ARCHIVO_VIAJES, ENCABEZADO_VIAJES, HORAS_ENTRE_VIAJES,
                    POSICION_NORTE, POSICION_SUR, TARIFA_BASE, TARIFA_MINIMA)
from entradas import confirmar, pedirEntero, pedirFecha, pedirHora
from listaenlazada import ListaEnlazada
from mensajes import advertencia, encabezado, error, exito, titulo
from viaje import Viaje

SENTIDO_NORTE = 1    # Concepción -> Santiago (posiciones de menor a mayor)
SENTIDO_SUR = -1     # Santiago -> Concepción (posiciones de mayor a menor)


# ---------------- Datos ----------------

def cargarViajes() -> ListaEnlazada:
    lista = ListaEnlazada()
    for datos in leerRegistros(ARCHIVO_VIAJES, ENCABEZADO_VIAJES):
        try:
            viaje = Viaje(datos[0], datos[1], datos[2], datos[3],
                          datos[4], datos[5], int(datos[6]))
            if not lista.agregar(viaje.id_viaje, viaje):
                advertencia(f"ID de viaje repetido en el archivo: {viaje.id_viaje}")
        except (ValueError, IndexError):
            advertencia(f"Línea inválida en viajes: {datos}")
    return lista


def listarViajes() -> list[Viaje]:
    return cargarViajes().recorrer()


def buscarxCodigo(id_viaje: str) -> Viaje | None:
    nodo = cargarViajes().buscarxCodigo(id_viaje)
    if nodo is not None:
        return nodo.dato
    return None


def guardarViaje(viaje: Viaje) -> bool:
    return agregarRegistro(ARCHIVO_VIAJES, ENCABEZADO_VIAJES, viaje.aLinea())


def sentidoViaje(viaje: Viaje) -> int:
    """Devuelve 1 si va al norte o -1 si va al sur (lo usan RF05 y RF06)."""
    origen = funcionesciudades.posicionCiudad(viaje.id_origen)
    destino = funcionesciudades.posicionCiudad(viaje.id_destino)
    if destino > origen:
        return SENTIDO_NORTE
    return SENTIDO_SUR


def recorrido(viaje: Viaje) -> str:
    return (funcionesciudades.nombreCiudad(viaje.id_origen) + " -> "
            + funcionesciudades.nombreCiudad(viaje.id_destino))


# ---------------- Validaciones ----------------

def buscarConflicto(id_bus: str, fecha: str, hora: str) -> Viaje | None:
    """Devuelve el viaje que choca si el bus ya sale con menos de HORAS_ENTRE_VIAJES de diferencia."""
    nuevo = datetime.strptime(fecha + " " + hora, "%Y-%m-%d %H:%M")
    for viaje in listarViajes():
        if viaje.id_bus == id_bus:
            try:
                diferencia = abs((viaje.fechaHora() - nuevo).total_seconds()) / 3600
                if diferencia < HORAS_ENTRE_VIAJES:
                    return viaje
            except ValueError:
                advertencia(f"El viaje {viaje.id_viaje} tiene fecha u hora inválida")
    return None


# ---------------- Opciones del menú ----------------

def programarViaje() -> None:
    titulo("Programar viaje")

    disponibles = []
    for bus in funcionesbuses.listarBuses():
        if bus.estaDisponible():
            disponibles.append(bus)

    if len(disponibles) == 0:
        error("No hay buses disponibles. Registre o habilite un bus primero")
        return

    encabezado("BUSES DISPONIBLES: ID | PATENTE | CAPACIDAD | ESTADO")
    for bus in disponibles:
        print(bus)

    id_bus = str(pedirEntero("\nIngrese ID del bus: ", 1, 999999))
    bus = funcionesbuses.buscarxCodigo(id_bus)
    if bus is None:
        error("El bus no existe")
        return
    if not bus.estaDisponible():
        error("El bus no está disponible")
        return

    fecha = pedirFecha("Ingrese fecha (AAAA-MM-DD): ")
    hora = pedirHora("Ingrese hora de salida (HH:MM): ")
    if datetime.strptime(fecha + " " + hora, "%Y-%m-%d %H:%M") < datetime.now():
        error("La fecha y hora de salida ya pasaron")
        return

    conflicto = buscarConflicto(id_bus, fecha, hora)
    if conflicto is not None:
        error(f"El bus ya tiene el viaje {conflicto.id_viaje} el {conflicto.fecha} a las "
              f"{conflicto.hora} (deben pasar {HORAS_ENTRE_VIAJES} horas entre viajes)")
        return

    sur = funcionesciudades.buscarxPosicion(POSICION_SUR)
    norte = funcionesciudades.buscarxPosicion(POSICION_NORTE)
    if sur is None or norte is None:
        error("El catálogo de ciudades está dañado")
        return

    print(f"""
    Sentido del viaje:
    1. {sur.nombre} -> {norte.nombre}
    2. {norte.nombre} -> {sur.nombre}""")
    sentido = pedirEntero("Seleccione sentido: ", 1, 2)
    if sentido == 1:
        id_origen = sur.id_ciudad
        id_destino = norte.id_ciudad
    else:
        id_origen = norte.id_ciudad
        id_destino = sur.id_ciudad

    if confirmar(f"¿Usar tarifa base de ${TARIFA_BASE}?"):
        tarifa = TARIFA_BASE
    else:
        tarifa = pedirEntero(f"Ingrese tarifa base (mínimo ${TARIFA_MINIMA}): ",
                             TARIFA_MINIMA, 1000000)

    id_viaje = str(cargarViajes().mayorCodigo() + 1)
    viaje = Viaje(id_viaje, id_bus, fecha, hora, id_origen, id_destino, tarifa)

    print(f"""
    RESUMEN DEL VIAJE
    RECORRIDO: {recorrido(viaje)}
    FECHA: {fecha}  HORA: {hora}
    BUS: {bus.patente}  TARIFA BASE: ${tarifa}""")

    if confirmar("¿Confirmar programación?"):
        if guardarViaje(viaje):
            exito(f"Viaje programado con ID {id_viaje}!!!")
    else:
        advertencia("Operación cancelada")


def mostrarViaje(viaje: Viaje) -> None:
    bus = funcionesbuses.buscarxCodigo(viaje.id_bus)
    if bus is not None:
        patente = bus.patente
    else:
        patente = "¿?"
    print(f"{viaje.id_viaje} | {viaje.fecha} {viaje.hora} | {recorrido(viaje)} | "
          f"{patente} | ${viaje.tarifa_base}")


def mostrarViajes() -> None:
    titulo("Viajes programados")
    viajes = listarViajes()
    if len(viajes) == 0:
        advertencia("No hay viajes programados")
        return
    encabezado("ID | FECHA HORA | RECORRIDO | BUS | TARIFA")
    for viaje in viajes:
        mostrarViaje(viaje)
    print(f"\nTotal: {len(viajes)} viajes")


def consultarViaje() -> None:
    titulo("Consultar viaje")
    id_viaje = str(pedirEntero("Ingrese ID del viaje: ", 1, 999999))
    viaje = buscarxCodigo(id_viaje)
    if viaje is None:
        error("Viaje no encontrado")
        return
    encabezado("ID | FECHA HORA | RECORRIDO | BUS | TARIFA")
    mostrarViaje(viaje)
    print(f"Capacidad del bus: {funcionesbuses.capacidadBus(viaje.id_bus)} asientos")


def menuViajes() -> None:
    while True:
        titulo("Gestión de viajes")
        print("""
    1. Programar viaje
    2. Listar viajes
    3. Consultar viaje
    0. Volver""")
        op = input("Ingrese una opción: ")
        match op:
            case "1":
                programarViaje()
            case "2":
                mostrarViajes()
            case "3":
                consultarViaje()
            case "0":
                break
            case other:
                error("Opción no válida!!!")
        input("Presione Enter para continuar...")
