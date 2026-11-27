import os

# Carpeta donde está este archivo (así funciona aunque se ejecute desde otra ruta)
RUTA = os.path.dirname(os.path.abspath(__file__))
CARPETA_DATOS = os.path.join(RUTA, "data")

ENCODE = "UTF-8"

ARCHIVO_BUSES = os.path.join(CARPETA_DATOS, "buses.csv")
ARCHIVO_CIUDADES = os.path.join(CARPETA_DATOS, "ciudades.csv")
ARCHIVO_VIAJES = os.path.join(CARPETA_DATOS, "viajes.csv")


ARCHIVO_PASAJES = os.path.join(CARPETA_DATOS, "pasajes.csv")
ENCABEZADO_PASAJES = "id_pasaje,id_viaje,id_cliente,id_origen,id_destino,asiento,valor,estado"
ESTADO_VIGENTE = "vigente"
ESTADO_ANULADO = "anulado"

ENCABEZADO_BUSES = "id_bus,patente,capacidad,estado"
ENCABEZADO_CIUDADES = "id_ciudad,nombre,posicion"
ENCABEZADO_VIAJES = "id_viaje,id_bus,fecha,hora,id_origen,id_destino,tarifa_base"

# Buses
ESTADO_DISPONIBLE = "disponible"
ESTADO_NO_DISPONIBLE = "no disponible"
CAPACIDAD_MAXIMA = 60

# Viajes
TARIFA_BASE = 10000
TARIFA_MINIMA = 1000
HORAS_ENTRE_VIAJES = 6  # un bus no puede tener dos viajes con menos de 6 horas de diferencia

# Ciudades: [id_ciudad, nombre, posicion] de sur a norte
CIUDADES = [
    ["1", "Concepción", "0"],
    ["2", "Chillán", "1"],
    ["3", "Linares", "2"],
    ["4", "Talca", "3"],
    ["5", "Rancagua", "4"],
    ["6", "Santiago", "5"],
]
POSICION_SUR = 0     # Concepción
POSICION_NORTE = 5   # Santiago


# Clientes
ARCHIVO_CLIENTES = os.path.join(CARPETA_DATOS, "clientes.csv")
ENCABEZADO_CLIENTES = "id_cliente,rut,nombres,apellido_paterno,apellido_materno,contacto"
