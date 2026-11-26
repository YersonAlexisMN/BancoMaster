
from archivos import leerRegistros, agregarRegistro, reescribirArchivo
from config import ARCHIVO_PASAJES, ENCABEZADO_PASAJES
from config import ESTADO_VIGENTE, ESTADO_ANULADO
from pasajes import Pasaje, calcularPrecio

from funcionesviajes import buscarxCodigo as buscarViaje
from funcionesviajes import sentidoViaje
from funcionesbuses import capacidadBus
from funcionesciudades import posicionCiudad
from funcionesclientes import buscarxCodigo as buscarCliente


def cargarPasajes() -> list[Pasaje]:
    pasajes = []
    registros = leerRegistros(ARCHIVO_PASAJES, ENCABEZADO_PASAJES)

    for datos in registros:
        try:
            if len(datos) == 8:
                pasaje = Pasaje(
                    datos[0],
                    datos[1],
                    datos[2],
                    datos[3],
                    datos[4],
                    int(datos[5]),
                    int(datos[6]),
                    datos[7]
                )
                pasajes.append(pasaje)
        except (ValueError, IndexError):
            print("Error: registro de pasaje inválido")

    return pasajes


def buscarxCodigo(id_pasaje: str) -> Pasaje | None:
    for pasaje in cargarPasajes():
        if pasaje.id_pasaje == id_pasaje:
            return pasaje

    return None


def guardarPasaje(pasaje: Pasaje) -> bool:
    if buscarxCodigo(pasaje.id_pasaje) is not None:
        return False

    linea = ",".join(pasaje.aLista())

    return agregarRegistro(
        ARCHIVO_PASAJES,
        ENCABEZADO_PASAJES,
        linea
    )


def validarTramo(viaje, id_origen: str, id_destino: str) -> bool:
    sentido = sentidoViaje(viaje)

    pos_inicio_viaje = posicionCiudad(viaje.id_origen)
    pos_final_viaje = posicionCiudad(viaje.id_destino)

    pos_origen = posicionCiudad(id_origen)
    pos_destino = posicionCiudad(id_destino)

    if sentido not in [1, -1]:
        return False

    if pos_inicio_viaje == -1 or pos_final_viaje == -1:
        return False

    if pos_origen == -1 or pos_destino == -1:
        return False

    if pos_origen == pos_destino:
        return False

    if sentido == 1:
        if pos_origen < pos_inicio_viaje or pos_destino > pos_final_viaje:
            return False

        if pos_destino < pos_origen:
            return False

    else:
        if pos_origen > pos_inicio_viaje or pos_destino < pos_final_viaje:
            return False

        if pos_destino > pos_origen:
            return False

    return True


def validarAsiento(id_viaje: str, asiento: int, id_origen: str, id_destino: str) -> bool:
    viaje = buscarViaje(id_viaje)

    if viaje is None:
        return False

    capacidad = capacidadBus(viaje.id_bus)

    if asiento < 1 or asiento > capacidad:
        return False

    if not validarTramo(viaje, id_origen, id_destino):
        return False

    sentido = sentidoViaje(viaje)

    pos_origen = posicionCiudad(id_origen) * sentido
    pos_destino = posicionCiudad(id_destino) * sentido

    for pasaje in cargarPasajes():
        if pasaje.id_viaje == id_viaje and pasaje.asiento == asiento:
            if pasaje.estado == ESTADO_VIGENTE:
                pos_inicio = posicionCiudad(pasaje.id_origen) * sentido
                pos_final = posicionCiudad(pasaje.id_destino) * sentido

                if pos_origen < pos_final and pos_inicio < pos_destino:
                    return False

    return True


def registrarPasaje(id_pasaje: str, id_viaje: str, id_cliente: str,
                    id_origen: str, id_destino: str, asiento: int) -> tuple[bool, str]:

    if buscarxCodigo(id_pasaje) is not None:
        return False, "El código de pasaje ya existe"

    viaje = buscarViaje(id_viaje)

    if viaje is None:
        return False, "El viaje no existe"

    cliente = buscarCliente(id_cliente)

    if cliente is None:
        return False, "El cliente no existe"

    if not validarTramo(viaje, id_origen, id_destino):
        return False, "El tramo seleccionado no corresponde al sentido del viaje"

    if not validarAsiento(id_viaje, asiento, id_origen, id_destino):
        return False, "El asiento no está disponible para ese tramo"

    pos_origen = posicionCiudad(id_origen)
    pos_destino = posicionCiudad(id_destino)

    valor = calcularPrecio(
        pos_origen,
        pos_destino,
        viaje.tarifa_base
    )

    pasaje = Pasaje(
        id_pasaje,
        id_viaje,
        id_cliente,
        id_origen,
        id_destino,
        asiento,
        valor,
        ESTADO_VIGENTE
    )

    if guardarPasaje(pasaje):
        return True, "Pasaje registrado correctamente"

    return False, "No se pudo guardar el pasaje"


def anularPasaje(id_pasaje: str) -> tuple[bool, str]:
    pasajes = cargarPasajes()
    encontrado = False

    for pasaje in pasajes:
        if pasaje.id_pasaje == id_pasaje:
            if pasaje.estado == ESTADO_ANULADO:
                return False, "El pasaje ya está anulado"

            pasaje.estado = ESTADO_ANULADO
            encontrado = True
            break

    if not encontrado:
        return False, "No existe un pasaje con ese código"

    lineas = []

    for pasaje in pasajes:
        lineas.append(",".join(pasaje.aLista()))

    if reescribirArchivo(ARCHIVO_PASAJES, ENCABEZADO_PASAJES, lineas):
        return True, "Pasaje anulado correctamente"

    return False, "No se pudo anular el pasaje"


def listarPasajesViaje(id_viaje: str) -> list[Pasaje]:
    pasajes = []

    for pasaje in cargarPasajes():
        if pasaje.id_viaje == id_viaje:
            pasajes.append(pasaje)

    return pasajes


def listarPasajesVigentes(id_viaje: str) -> list[Pasaje]:
    pasajes = []

    for pasaje in cargarPasajes():
        if pasaje.id_viaje == id_viaje and pasaje.estado == ESTADO_VIGENTE:
            pasajes.append(pasaje)

    return pasajes


def ordenarManifiesto(pasajes: list[Pasaje]) -> list[Pasaje]:
    i = 0

    while i < len(pasajes) - 1:
        j = 0

        while j < len(pasajes) - 1 - i:
            if pasajes[j].asiento > pasajes[j + 1].asiento:
                auxiliar = pasajes[j]
                pasajes[j] = pasajes[j + 1]
                pasajes[j + 1] = auxiliar

            j = j + 1

        i = i + 1

    return pasajes


def manifiesto(id_viaje: str) -> list[Pasaje]:
    pasajes = listarPasajesVigentes(id_viaje)

    return ordenarManifiesto(pasajes)


def calcularRecaudacion(id_viaje: str) -> int:
    total = 0

    for pasaje in listarPasajesVigentes(id_viaje):
        total = total + pasaje.valor

    return total


def contarPasajesVigentes(id_viaje: str) -> int:
    total = 0

    for pasaje in listarPasajesVigentes(id_viaje):
        total = total + 1

    return total


def asientosOcupados(id_viaje: str, id_origen: str, id_destino: str) -> list[int]:
    ocupados = []

    viaje = buscarViaje(id_viaje)

    if viaje is None:
        return ocupados

    sentido = sentidoViaje(viaje)

    if not validarTramo(viaje, id_origen, id_destino):
        return ocupados

    pos_origen = posicionCiudad(id_origen) * sentido
    pos_destino = posicionCiudad(id_destino) * sentido

    for pasaje in listarPasajesVigentes(id_viaje):
        pos_inicio = posicionCiudad(pasaje.id_origen) * sentido
        pos_final = posicionCiudad(pasaje.id_destino) * sentido

        if pos_origen < pos_final and pos_inicio < pos_destino:
            if pasaje.asiento not in ocupados:
                ocupados.append(pasaje.asiento)

    return ocupados


def asientosDisponibles(id_viaje: str, id_origen: str, id_destino: str) -> list[int]:
    disponibles = []

    viaje = buscarViaje(id_viaje)

    if viaje is None:
        return disponibles

    capacidad = capacidadBus(viaje.id_bus)
    ocupados = asientosOcupados(id_viaje, id_origen, id_destino)

    asiento = 1

    while asiento <= capacidad:
        if asiento not in ocupados:
            disponibles.append(asiento)

        asiento = asiento + 1

    return disponibles
