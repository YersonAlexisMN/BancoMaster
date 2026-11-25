from datetime import datetime, date

from mensajes import error


def pedirTexto(mensaje: str) -> str:
    while True:
        texto = input(mensaje).strip()
        if len(texto) > 0:
            return texto
        else:
            error("El campo no puede estar vacío")


def pedirEntero(mensaje: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo and numero <= maximo:
                return numero
            else:
                raise Exception(f"Debe ingresar un valor entre {minimo} y {maximo}")
        except ValueError:
            error("Debe ingresar un valor numérico entero")
        except Exception as err:
            error(str(err))


def pedirFecha(mensaje: str) -> str:
    """Pide una fecha AAAA-MM-DD que no sea anterior a hoy."""
    while True:
        texto = input(mensaje).strip()
        try:
            fecha = datetime.strptime(texto, "%Y-%m-%d").date()
            if fecha >= date.today():
                return texto
            else:
                raise Exception("La fecha no puede ser anterior a hoy")
        except ValueError:
            error("Formato inválido, use AAAA-MM-DD (ejemplo: 2026-12-15)")
        except Exception as err:
            error(str(err))


def pedirHora(mensaje: str) -> str:
    """Pide una hora HH:MM y la devuelve con dos dígitos (8:5 -> 08:05)."""
    while True:
        texto = input(mensaje).strip()
        try:
            hora = datetime.strptime(texto, "%H:%M")
            return hora.strftime("%H:%M")
        except ValueError:
            error("Formato inválido, use HH:MM (ejemplo: 08:30)")


def confirmar(mensaje: str) -> bool:
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta == "s":
            return True
        elif respuesta == "n":
            return False
        else:
            error("Debe responder s o n")
