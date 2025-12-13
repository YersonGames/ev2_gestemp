import prettytable
import mysql.connector
import time

# Clases

# Servicios 
import MenuGestionDestinos
import MenuGestionPaquetes
import servicios.LimpiarPantalla as screen
from servicios.EncriptarDesencriptar import encriptar,desencriptar

def mostrar_menu_gestion_viajes():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Gestionar Destinos"],
                    [2,"Gestionar Paquetes"],
                    [0,"Volver"]
                  ])
    print(menu)

def menu_gestion_viajes(connect):
    conexion = connect
    salir = 0
    while salir == 0:
        mostrar_menu_gestion_viajes()
        opcion = input("Opcion: ")

        #Gestion de Destinos
        if opcion == "1":
            MenuGestionDestinos.menu_gestion_destinos(conexion)
        elif opcion == "2":
            MenuGestionPaquetes.menu_gestion_paquetes(conexion)
        elif opcion == "0":
            salir = 1