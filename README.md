# RutaSur Transportes

## Descripción
Proyecto grupal desarrollado en Python para la gestión de una empresa de transporte terrestre. El sistema contempla la administración de buses, ciudades, viajes, clientes y pasajes, utilizando archivos CSV para almacenar información.

## Estado del trabajo compartido

### Módulo de pasajes — rama `phillips`
Se desarrolló una primera versión del módulo de pasajes, que incluye:

- Clase `Pasaje` y sus atributos.
- Cálculo del precio según el tramo del viaje.
- Búsqueda y registro de pasajes.
- Validación de tramos y asientos.
- Anulación de pasajes.
- Listado de pasajes por viaje y pasajes vigentes.
- Generación del manifiesto de pasajeros.
- Cálculo de recaudación y disponibilidad de asientos.

### Módulo de clientes
Se preparó una implementación local que incluye:

- Clase `Cliente`.
- Registro y listado de clientes.
- Búsqueda por código y RUT.
- Modificación de datos de clientes.
- Almacenamiento mediante los métodos de `archivos.py`.

Estos archivos se están incorporando a la rama `phillips` para que el equipo pueda revisarlos e integrarlos.

### Otros módulos
El repositorio también contiene archivos relacionados con buses, ciudades, viajes, configuración, entradas, mensajes y manejo de archivos. La integración general debe ser revisada por el equipo.

## Problemas y tareas pendientes

1. **Integración de clientes:** en la última revisión de `origin/yerson`, `clientes.py` y `funcionesclientes.py` aparecían vacíos y `cliente.py` no existía. Se preparó una versión local en la rama `phillips`; debe compararse con la versión definitiva de Yerson para evitar duplicaciones o incompatibilidades.

2. **Formato de pasajes:** revisar la conversión de los objetos `Pasaje` a líneas de texto, ya que las funciones de escritura de `archivos.py` reciben líneas de texto. La clase actualmente dispone de `aLista()` y debe comprobarse su compatibilidad con las funciones de guardado.

3. **Manifiesto:** revisar el orden solicitado para los pasajeros. La versión actual debe comprobarse para asegurar que ordene por apellido, nombres y número de asiento, según corresponda.

4. **Dependencias entre módulos:** verificar que los nombres de funciones y las importaciones coincidan entre pasajes, viajes, buses, ciudades y clientes.

5. **Menús e integración:** comprobar que el menú de pasajes y los demás menús estén conectados correctamente al programa principal.

6. **Pruebas generales:** ejecutar pruebas de registro, búsqueda, modificación, anulación, validación de asientos, lectura y escritura de archivos CSV.

7. **Ejecución local:** queda pendiente completar la prueba de ejecución del proyecto en el entorno local.

## Indicaciones para la integración

- La rama `phillips` contiene el trabajo del módulo de pasajes y los archivos locales preparados para clientes.
- La rama `yerson` debe revisarse para confirmar que sus archivos definitivos estén publicados.
- La integración final en `main` queda a cargo de quien coordine la integración del proyecto.
- Antes de integrar, revisar las importaciones, nombres de archivos, funciones y encabezados CSV para evitar incompatibilidades.

## Importante
Este documento describe el estado del trabajo al momento de su entrega. Los módulos y funcionalidades mencionados deben revisarse y probarse en conjunto antes de considerar el proyecto completamente integrado y terminado.
