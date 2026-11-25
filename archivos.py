import os

from config import CARPETA_DATOS, ENCODE
from mensajes import error


def verificarArchivo(archivo: str, encabezado: str) -> None:
    """Si el archivo no existe o está vacío, lo crea con su encabezado."""
    try:
        if not os.path.exists(CARPETA_DATOS):
            os.makedirs(CARPETA_DATOS)
        if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
            f = open(archivo, "w", encoding=ENCODE)
            f.write(encabezado + "\n")
            f.close()
    except OSError as err:
        error(f"No se pudo crear el archivo {archivo}: {err}")


def leerRegistros(archivo: str, encabezado: str) -> list[list[str]]:
    """Devuelve cada línea del archivo como lista de datos, sin el encabezado."""
    verificarArchivo(archivo, encabezado)
    registros = []
    try:
        f = open(archivo, "r", encoding=ENCODE)
        lineas = f.readlines()
        f.close()
        for linea in lineas[1:]:          # se salta el encabezado
            linea = linea.replace("\n", "")
            if linea.strip() != "":       # se saltan líneas vacías
                datos = linea.split(",")
                registros.append(datos)
    except OSError as err:
        error(f"No se pudo leer el archivo {archivo}: {err}")
    return registros


def agregarRegistro(archivo: str, encabezado: str, linea: str) -> bool:
    """Agrega una línea al final del archivo."""
    verificarArchivo(archivo, encabezado)
    try:
        f = open(archivo, "a", encoding=ENCODE)
        f.write(linea + "\n")
        f.close()
        return True
    except OSError as err:
        error(f"No se pudo guardar en {archivo}: {err}")
        return False


def reescribirArchivo(archivo: str, encabezado: str, lineas: list[str]) -> bool:
    """Borra el archivo y lo vuelve a escribir completo (se usa al modificar)."""
    try:
        f = open(archivo, "w", encoding=ENCODE)
        f.write(encabezado + "\n")
        for linea in lineas:
            f.write(linea + "\n")
        f.close()
        return True
    except OSError as err:
        error(f"No se pudo guardar en {archivo}: {err}")
        return False
