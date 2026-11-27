from os import system

import funcionesbuses
import funcionesciudades
import funcionesclientes
import funcionespasajes
import funcionesviajes
from mensajes import error, exito, titulo

system("cls")
funcionesciudades.crearCiudades()

while True:
    titulo("RutaSur Transportes")
    print("""
    1. Buses
    2. Ciudades
    3. Viajes
    4. Clientes
    5. Pasajes y reportes
    0. Salir""")
    op = input("Ingrese una opción: ")
    match op:
        case "1":
            funcionesbuses.menuBuses()
        case "2":
            funcionesciudades.mostrarCiudades()
            input("Presione Enter para continuar...")
        case "3":
            funcionesviajes.menuViajes()
        case "4":
            funcionesclientes.menuClientes()
        case "5":
            funcionespasajes.menuPasajes()
        case "0":
            exito("Fin del programa....")
            break
        case other:
            error("Opción no válida!!!")
    system("cls")