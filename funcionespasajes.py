

from archivos import leerRegistros, agregarRegistro, reescribirArchivo
from config import ARCHIVO_PASAJES, ENCABEZADO_PASAJES
from config import ESTADO_VIGENTE, ESTADO_ANULADO
from pasajes import Pasaje, calcularPrecio

from funcionesviajes import buscarxCodigo as buscarViaje
from funcionesviajes import sentidoViaje
from funcionesbuses import capacidadBus
from funcionesciudades import posicionCiudad
from funcionesclientes import buscarxCodigo as buscarCliente

import funcionesciudades
import funcionesviajes

from entradas import confirmar, pedirEntero
from mensajes import advertencia, encabezado, error, exito, titulo



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

    linea = pasaje.aLinea()

    return agregarRegistro(
        ARCHIVO_PASAJES,
        ENCABEZADO_PASAJES,
        linea
    )


def validarTramo(viaje: Viaje, id_origen: str, id_destino: str) -> bool:    sentido = sentidoViaje(viaje)

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
        lineas.append(pasaje.aLinea())

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
    pasajes = pasajes.copy()
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


def normalizar(texto: str) -> str:
    texto = texto.lower()
    cambios = {
        "á": "a", "é": "e", "í": "i",
        "ó": "o", "ú": "u", "ü": "u", "ñ": "n~"
    }

    resultado = ""

    for letra in texto:
        if letra in cambios:
            resultado += cambios[letra]
        else:
            resultado += letra

    return resultado


def claveOrden(fila: list, criterio: str) -> list:
    if criterio == "apellido":
        return [normalizar(fila[1]), normalizar(fila[2]), normalizar(fila[3]), fila[0]]

    elif criterio == "nombres":
        return [normalizar(fila[3]), normalizar(fila[1]), fila[0]]

    else:
        return [fila[0], fila[6]]


def ordenarNomina(nomina: list, criterio: str) -> list:
    lista = nomina.copy()
    n = len(lista)

    for i in range(n - 1):
        hubo_cambio = False

        for j in range(n - 1 - i):
            if claveOrden(lista[j], criterio) > claveOrden(lista[j + 1], criterio):
                auxiliar = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = auxiliar
                hubo_cambio = True

        if not hubo_cambio:
            break

    return lista


def armarNomina(id_viaje: str) -> list:
    nomina = []

    for pasaje in listarPasajesVigentes(id_viaje):
        cliente = buscarCliente(pasaje.id_cliente)

        if cliente is not None:
            nomina.append([
                pasaje.asiento,
                cliente.apellido_paterno,
                cliente.apellido_materno,
                cliente.nombres,
                funcionesciudades.nombreCiudad(pasaje.id_origen),
                funcionesciudades.nombreCiudad(pasaje.id_destino),
                posicionCiudad(pasaje.id_origen),
            ])

    return nomina


def siguienteIdPasaje() -> str:
    mayor = 0

    for pasaje in cargarPasajes():
        if pasaje.id_pasaje.isdigit() and int(pasaje.id_pasaje) > mayor:
            mayor = int(pasaje.id_pasaje)

    return str(mayor + 1)


def pedirViaje() -> Viaje | None:
    id_viaje = str(pedirEntero("Ingrese ID del viaje: ", 1, 999999))
    viaje = buscarViaje(id_viaje)

    if viaje is None:
        error("Viaje no encontrado")

    return viaje


def elegirCiudad(mensaje: str) -> str:
    ciudades = funcionesciudades.listarCiudades()

    print(mensaje)

    for ciudad in ciudades:
        print(f"    {ciudad.id_ciudad}. {ciudad.nombre}")

    if len(ciudades) == 0:
        error("No hay ciudades registradas")
        return ""

    opcion = pedirEntero("Seleccione ciudad: ", 1, len(ciudades))

    return str(ciudades[opcion - 1].id_ciudad)


def mostrarViajeElegido(viaje: Viaje) -> None:    print(f"\n    VIAJE {viaje.id_viaje}: {funcionesviajes.recorrido(viaje)} | "
          f"{viaje.fecha} {viaje.hora} | tarifa base ${viaje.tarifa_base} | "
          f"capacidad {capacidadBus(viaje.id_bus)} asientos")


def venderPasaje() -> None:
    titulo("Vender pasaje")
    viaje = pedirViaje()

    if viaje is None:
        return

    mostrarViajeElegido(viaje)

    id_cliente = str(pedirEntero("Ingrese ID del cliente: ", 1, 999999))
    cliente = buscarCliente(id_cliente)

    if cliente is None:
        error("El cliente no existe")
        return

    print(f"    CLIENTE: {cliente.nombres} {cliente.apellido_paterno} {cliente.apellido_materno}")

    id_origen = elegirCiudad("\n    Ciudad de embarque:")
    id_destino = elegirCiudad("\n    Ciudad de destino:")

    if id_origen == "" or id_destino == "":
        return

    if id_origen == id_destino:
        error("El origen no puede ser igual al destino")
        return

    if not validarTramo(viaje, id_origen, id_destino):
        error("El tramo no corresponde al sentido del viaje")
        return

    disponibles = asientosDisponibles(viaje.id_viaje, id_origen, id_destino)

    if len(disponibles) == 0:
        error("No quedan asientos disponibles para ese tramo")
        return

    print(f"\n    Asientos disponibles en ese tramo: {disponibles}")

    asiento = pedirEntero(
        f"Ingrese número de asiento (1 a {capacidadBus(viaje.id_bus)}): ",
        1,
        capacidadBus(viaje.id_bus)
    )

    if asiento not in disponibles:
        error(f"El asiento {asiento} está ocupado en un tramo que se superpone")
        return

    valor = calcularPrecio(
        posicionCiudad(id_origen),
        posicionCiudad(id_destino),
        viaje.tarifa_base
    )

    print(f"""
    RESUMEN DEL PASAJE
    TRAMO: {funcionesciudades.nombreCiudad(id_origen)} -> {funcionesciudades.nombreCiudad(id_destino)}
    ASIENTO: {asiento}
    VALOR: ${valor}""")

    if not confirmar("¿Confirmar venta?"):
        advertencia("Operación cancelada")
        return

    ok, mensaje = registrarPasaje(
        siguienteIdPasaje(),
        viaje.id_viaje,
        id_cliente,
        id_origen,
        id_destino,
        asiento
    )

    if ok:
        exito(mensaje + "!!!")
    else:
        error(mensaje)


def anularPasajeMenu() -> None:
    titulo("Anular pasaje")
    id_pasaje = str(pedirEntero("Ingrese ID del pasaje: ", 1, 999999))
    pasaje = buscarxCodigo(id_pasaje)

    if pasaje is None:
        error("No existe un pasaje con ese código")
        return

    print(f"    Pasaje {pasaje.id_pasaje} | viaje {pasaje.id_viaje} | asiento {pasaje.asiento} | "
          f"{funcionesciudades.nombreCiudad(pasaje.id_origen)} -> "
          f"{funcionesciudades.nombreCiudad(pasaje.id_destino)} | {pasaje.estado}")

    if not confirmar("¿Anular este pasaje?"):
        advertencia("Operación cancelada")
        return

    ok, mensaje = anularPasaje(id_pasaje)

    if ok:
        exito(mensaje + ". El asiento quedó libre solo en ese tramo")
    else:
        error(mensaje)


def mostrarPasajesViaje() -> None:
    titulo("Pasajes de un viaje")
    viaje = pedirViaje()

    if viaje is None:
        return

    mostrarViajeElegido(viaje)
    pasajes = listarPasajesViaje(viaje.id_viaje)

    if len(pasajes) == 0:
        advertencia("El viaje no tiene pasajes")
        return

    encabezado("ID | ASIENTO | CLIENTE | TRAMO | VALOR | ESTADO")

    for p in pasajes:
        cliente = buscarCliente(p.id_cliente)
        nombre = cliente.nombres + " " + cliente.apellido_paterno if cliente else "¿?"

        linea = (f"{p.id_pasaje} | {p.asiento} | {nombre} | "
                 f"{funcionesciudades.nombreCiudad(p.id_origen)} -> "
                 f"{funcionesciudades.nombreCiudad(p.id_destino)} | ${p.valor} | {p.estado.upper()}")

        if p.estado == ESTADO_ANULADO:
            advertencia(linea)
        else:
            print(linea)


def mostrarNomina() -> None:
    titulo("Nómina de pasajeros")
    viaje = pedirViaje()

    if viaje is None:
        return

    mostrarViajeElegido(viaje)
    nomina = armarNomina(viaje.id_viaje)

    if len(nomina) == 0:
        advertencia("El viaje no tiene pasajes vigentes")
        return

    print("""
    Ordenar por:
    1. Apellido paterno
    2. Nombres
    3. Número de asiento""")

    opcion = pedirEntero("Seleccione: ", 1, 3)
    criterios = ["apellido", "nombres", "asiento"]
    ordenada = ordenarNomina(nomina, criterios[opcion - 1])

    encabezado("ASIENTO | AP. PATERNO | AP. MATERNO | NOMBRES | EMBARQUE | DESTINO")

    for f in ordenada:
        print(f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]}")

    print(f"\nTotal: {len(ordenada)} pasajeros")


def mostrarRecaudacion() -> None:
    titulo("Recaudación del viaje")
    viaje = pedirViaje()

    if viaje is None:
        return

    mostrarViajeElegido(viaje)
    exito(f"Pasajes vigentes: {contarPasajesVigentes(viaje.id_viaje)}")
    exito(f"Recaudación vigente: ${calcularRecaudacion(viaje.id_viaje)} (no incluye anulados)")


def mostrarOcupacion() -> None:
    titulo("Ocupación de asientos por tramo")
    viaje = pedirViaje()

    if viaje is None:
        return

    mostrarViajeElegido(viaje)
    id_origen = elegirCiudad("\n    Desde:")
    id_destino = elegirCiudad("\n    Hasta:")

    if id_origen == "" or id_destino == "":
        return

    if not validarTramo(viaje, id_origen, id_destino):
        error("El tramo no corresponde al sentido del viaje")
        return

    ocupados = asientosOcupados(viaje.id_viaje, id_origen, id_destino)
    disponibles = asientosDisponibles(viaje.id_viaje, id_origen, id_destino)

    encabezado(f"TRAMO {funcionesciudades.nombreCiudad(id_origen)} -> "
               f"{funcionesciudades.nombreCiudad(id_destino)}")

    advertencia(f"Ocupados ({len(ocupados)}): {ocupados}")
    exito(f"Disponibles ({len(disponibles)}): {disponibles}")


def menuPasajes() -> None:
    while True:
        titulo("Pasajes y reportes")

        print("""
    1. Vender pasaje
    2. Anular pasaje
    3. Pasajes vigentes y anulados de un viaje
    4. Nómina de pasajeros
    5. Recaudación de un viaje
    6. Ocupación de asientos por tramo
    0. Volver""")

        op = input("Ingrese una opción: ")

        match op:
            case "1":
                venderPasaje()
            case "2":
                anularPasajeMenu()
            case "3":
                mostrarPasajesViaje()
            case "4":
                mostrarNomina()
            case "5":
                mostrarRecaudacion()
            case "6":
                mostrarOcupacion()
            case "0":
                break
            case other:
                error("Opción no válida!!!")

        input("Presione Enter para continuar...")
