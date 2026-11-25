# RF03 · Catálogo de ciudades (solo consulta)
from archivos import leerRegistros, reescribirArchivo
from ciudad import Ciudad
from config import ARCHIVO_CIUDADES, ENCABEZADO_CIUDADES, CIUDADES
from mensajes import encabezado, titulo, advertencia


def crearCiudades() -> None:
    """Si el archivo no tiene las 6 ciudades, lo vuelve a crear con el catálogo fijo."""
    registros = leerRegistros(ARCHIVO_CIUDADES, ENCABEZADO_CIUDADES)
    if len(registros) != len(CIUDADES):
        if len(registros) > 0:
            advertencia("El catálogo de ciudades estaba incompleto, se restauró")
        lineas = []
        for c in CIUDADES:
            lineas.append(f"{c[0]},{c[1]},{c[2]}")
        reescribirArchivo(ARCHIVO_CIUDADES, ENCABEZADO_CIUDADES, lineas)


def listarCiudades() -> list[Ciudad]:
    crearCiudades()
    ciudades = []
    for datos in leerRegistros(ARCHIVO_CIUDADES, ENCABEZADO_CIUDADES):
        try:
            ciudad = Ciudad(datos[0], datos[1], int(datos[2]))
            ciudades.append(ciudad)
        except (ValueError, IndexError):
            advertencia(f"Línea inválida en ciudades: {datos}")
    return ciudades


def buscarxCodigo(id_ciudad: str) -> Ciudad | None:
    for ciudad in listarCiudades():
        if ciudad.id_ciudad == id_ciudad:
            return ciudad
    return None


def buscarxPosicion(posicion: int) -> Ciudad | None:
    for ciudad in listarCiudades():
        if ciudad.posicion == posicion:
            return ciudad
    return None


def nombreCiudad(id_ciudad: str) -> str:
    ciudad = buscarxCodigo(id_ciudad)
    if ciudad is not None:
        return ciudad.nombre
    return "¿?"


def posicionCiudad(id_ciudad: str) -> int:
    """Devuelve la posición de la ciudad o -1 si no existe."""
    ciudad = buscarxCodigo(id_ciudad)
    if ciudad is not None:
        return ciudad.posicion
    return -1


def mostrarCiudades() -> None:
    titulo("Catálogo de ciudades (sur a norte)")
    encabezado("ID | CIUDAD | POSICIÓN")
    for ciudad in listarCiudades():
        print(ciudad)
