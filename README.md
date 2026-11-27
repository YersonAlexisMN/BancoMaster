# RutaSur Transportes

Proyecto de la evaluación integradora de Estructuras de Datos, UTFSM.

Integrantes:
- Dante (Dconcham28): buses, ciudades, viajes y los archivos base del proyecto.
- Yerson Alveal (YersonAlexisMN): clientes.
- Phillips Rubilar (PhillipsRubilar19): pasajes, anulación, nómina y reportes.

## De qué se trata

Hicimos un programa de consola en Python para una empresa de buses que viaja entre Concepción y Santiago, pasando por Chillán, Linares, Talca y Rancagua. Permite registrar clientes, buses y viajes, vender pasajes por tramo, anularlos y ver la nómina de pasajeros. Toda la información se guarda en archivos CSV dentro de la carpeta `data`, y los archivos se relacionan entre sí por ID (por ejemplo, un pasaje guarda el id del viaje y el id del cliente, no sus datos completos).

## Instalación y ejecución

Hay que tener Python 3.10 o superior. Después de clonar el repositorio se instala colorama, que es lo que usamos para los colores:

```
pip install -r requirements.txt
```

Y para ejecutar:

```
python main.py
```

Si los archivos de `data` no existen o están vacíos, el programa los crea solo al abrirse.

## Cómo lo organizamos

Tratamos de seguir la forma en que trabajamos en clases: cada entidad tiene su clase en un archivo (`bus.py`, `viaje.py`, `ciudad.py`, `cliente.py`, `pasajes.py`) y sus funciones en otro (`funcionesbuses.py`, `funcionesviajes.py`, etc.). Además hay unos archivos que usamos todos: `config.py` con las rutas y constantes, `archivos.py` para leer y guardar los CSV, `entradas.py` para pedir datos validando lo que escribe el usuario, y `mensajes.py` para los colores. El menú principal está en `main.py`. Todas las funciones tienen tipado.

## Estructuras y algoritmos

Usamos una lista enlazada (`listaenlazada.py`) para cargar los buses, viajes y clientes cuando se leen los archivos. Cada nodo guarda el ID y el objeto, y apunta al siguiente. Nos sirvió para buscar por ID recorriendo los nodos, para no dejar entrar IDs repetidos y para sacar el siguiente ID cuando se registra algo nuevo.

Para ordenar la nómina usamos el método de la burbuja, porque no se podía usar sort(). Se va comparando cada pasajero con el siguiente y se cambian de lugar si están en el orden equivocado, hasta que ya no haya cambios. Lo elegimos porque es el que vimos en clases y para una lista del tamaño de un bus funciona bien. Se puede ordenar por apellido paterno, por nombres o por asiento. Si hay empate, por apellido se mira después el apellido materno y los nombres; por nombres se mira el apellido; y por asiento (cuando el mismo asiento se usa en tramos distintos) se ordena según la ciudad donde se sube. Antes de comparar sacamos las tildes para que, por ejemplo, Ávila quede antes que Bravo. El orden se hace sobre una copia, así que no cambia el archivo.

También usamos búsqueda secuencial para cosas como buscar un bus por patente o un cliente por RUT.

## Algunas reglas que validamos

El precio del pasaje se calcula solo: por cada tramo del recorrido que no se usa se descuenta un 10% de la tarifa base. Un asiento se puede vender varias veces en el mismo viaje si los tramos no se topan, por ejemplo Concepción-Chillán y después Chillán-Talca. Al anular un pasaje no se borra, solo cambia su estado, y así el asiento queda libre únicamente en ese tramo; los anulados no cuentan en la recaudación.

Otras validaciones: el RUT se revisa con su dígito verificador y no se puede repetir, la patente tiene formato chileno y tampoco se repite, la capacidad del bus va de 1 a 60, los viajes solo pueden ser Concepción-Santiago o al revés, y un mismo bus no puede tener dos viajes con menos de 6 horas de diferencia.

## Pruebas

Probamos los casos que pedía el enunciado (RUT y patente repetidos, tarifas, asientos en tramos que se topan y que no, anulación, nómina ordenada, recaudación y cerrar y abrir el programa). Las capturas están en la carpeta `evidencias`.

## Git

Cada uno trabajó en su propia rama (dante, yerson y phillips) y al final juntamos todo en main con merge.
